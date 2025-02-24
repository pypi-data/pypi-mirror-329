from __future__ import annotations

import asyncio
import collections.abc
import pathlib
import sys
import typing
import zipfile

from asyncio_extras import call_in_executor, open_async
from momotor.shared.doc import annotate_docstring
from momotor.shared.log import getAsyncLogger

from momotor.rpc.asset.exceptions import AssetHashMismatchError, \
    AssetSizeMismatchError, UnexpectedEndOfStream
from momotor.rpc.asset.utils import file_reader, file_writer, get_file_hash, \
    get_file_multihash
from momotor.rpc.const import CHUNK_SIZE
from momotor.rpc.exception import raise_message_exception
from momotor.rpc.hash import decode as decode_hash
from momotor.rpc.hash import is_identity_code
from momotor.rpc.proto.asset_pb2 import XML, ZIP, AssetData, AssetQuery, \
    Category, DownloadAssetRequest, UploadAssetRequest
from momotor.rpc.proto.auth_pb2 import ServerInfoResponse
from momotor.rpc.proto.client_grpc import ClientStub
from momotor.rpc.proto.worker_grpc import WorkerStub

try:
    from typing import TypeAlias  # type: ignore py3.10+
except ImportError:
    from typing_extensions import TypeAlias

if sys.version_info >= (3, 10):
    StubType: TypeAlias = "ClientStub | WorkerStub"
else:
    StubType = typing.Union["ClientStub", "WorkerStub"]

if typing.TYPE_CHECKING:
    from concurrent.futures import Executor


logger = getAsyncLogger(__name__)

# Remote (clients and workers) side of asset up/downloading.
# Counterpart is in server.py

@annotate_docstring(logger=logger)
async def send_asset(stub: StubType, job_id: str, query: AssetQuery, path: str | pathlib.Path,
                     server_info: ServerInfoResponse, *,
                     process_executor: "Executor | None" = None, timeout: float | None = None) -> None:
    """ Function for use by a client or worker to send an asset to the broker server

    Produces log messages on the ``{logger.name}`` logger.

    :param stub: The connected stub to the broker.
    :param job_id: Id of the job
    :param query: Query for the asset
    :param path: Local file path of the file to send
    :param server_info: The server's info response
    :param process_executor: An asyncio executor to execute long running CPU bound tasks
    :param timeout: Timeout
    """

    path = pathlib.Path(path)

    stat, hash_data, is_zip = await asyncio.gather(
        call_in_executor(path.stat),
        call_in_executor(get_file_multihash, path, server_info, executor=process_executor),  # type: ignore
        call_in_executor(zipfile.is_zipfile, path)
    ) # type: ignore
    
    size = stat.st_size
    hash_value, identity_hash = hash_data
    data = AssetData(
        query=query,
        format=ZIP if is_zip else XML,
        size=size,
        hash=hash_value,
    )
    cat_name = Category.Name(query.category)

    async with stub.uploadAsset.open() as stream:
        await logger.debug(f"sending {cat_name}")

        try:
            await asyncio.wait_for(
                stream.send_message(UploadAssetRequest(jobId=job_id, assetData=data)),
                timeout=timeout
            )

            response = await stream.recv_message()
            raise_message_exception(response)
            assert response is not None

            if response.assetSelected:
                await logger.debug(f"sending {cat_name} accepted, asset known")
            elif identity_hash:
                await logger.debug(f"sending {cat_name} accepted, asset unknown, id-encoded")
            else:
                await logger.debug(f"sending {cat_name} accepted, asset unknown")

                if server_info:
                    chunk_size = min(server_info.chunkSize, CHUNK_SIZE)
                else:
                    chunk_size = CHUNK_SIZE

                read_queue = asyncio.Queue(1)
                read_task = asyncio.ensure_future(file_reader(path, 'rb', read_queue, chunk_size=chunk_size))
                try:
                    count = 0
                    while True:
                        chunk = await read_queue.get()
                        if not chunk:
                            break

                        count += 1
                        await logger.debug(f"sending {cat_name} chunk {count}")
                        await asyncio.wait_for(
                            stream.send_message(UploadAssetRequest(chunk=chunk)),
                            timeout=timeout
                        )
                finally:
                    await read_task

            await logger.debug(f"sending {cat_name} done")

        finally:
            try:
                await stream.end()
            except Exception as exc:
                await logger.warning(f"unable to end stream: {exc}")


@annotate_docstring(logger=logger)
async def receive_asset(stub: StubType, job_id: str, query: AssetQuery, path: str | pathlib.Path,
                        exists: collections.abc.Callable[[AssetData], collections.abc.Awaitable[bool]] | None = None,
                        process_executor: "Executor | None" = None, timeout: float | None = None) -> tuple[AssetData, bool]:
    """ Function for use by a client or worker to request and receive an asset from the broker.

    Produces log messages on the ``{logger.name}`` logger.

    :param stub: The connected stub to the broker.
    :param job_id: Id of the job
    :param query: Query for the asset
    :param path: Local file path where the file is to be stored
    :param exists: A function that checks if the file is already known locally
    :param process_executor: An asyncio executor to execute long running CPU bound tasks
    :param timeout: Timeout
    :return: A tuple with the :py:class:`~momotor.rpc.proto.asset_pb2.AssetData` identifying the asset, and
             a boolean indicating whether the asset already exists locally.
    """

    cat_name = Category.Name(query.category)

    async with stub.downloadAsset.open() as stream:
        await logger.debug(f"receiving {cat_name}")

        await asyncio.wait_for(
            stream.send_message(DownloadAssetRequest(jobId=job_id, query=query)),
            timeout=timeout
        )

        response = await stream.recv_message()
        raise_message_exception(response)
        assert response is not None

        data = response.data

        hash_digest, hash_code = decode_hash(data.hash)
        is_identity_hash = is_identity_code(hash_code)

        existing = not is_identity_hash and (await exists(data) if callable(exists) else False)
        await asyncio.wait_for(
            stream.send_message(DownloadAssetRequest(accepted=is_identity_hash or not existing), end=True),
            timeout=timeout
        )

        if existing:
            await logger.debug(f"receiving {cat_name} accepted, asset known")
        elif data.size == 0:
            await logger.debug(f"receiving {cat_name} accepted, asset empty")
        elif is_identity_hash:
            await logger.debug(f"receiving {cat_name} accepted, asset received as identity-hash")

            if data.size != len(hash_digest):
                raise AssetHashMismatchError("Hash size mismatch")

            async with open_async(path, 'wb') as f:
                await f.write(hash_digest)

        else:
            await logger.debug(f"receiving {cat_name} accepted, asset unknown")

            count, remaining = 0, data.size

            write_queue = asyncio.Queue(1)
            write_task = asyncio.ensure_future(file_writer(path, 'wb', write_queue))  # type: ignore
            try:
                while remaining > 0:
                    chunk = response.chunk
                    if len(chunk) > remaining:
                        raise AssetSizeMismatchError

                    if chunk:
                        await write_queue.put(chunk)
                        remaining -= len(chunk)

                    if remaining > 0:
                        count += 1
                        await logger.debug(f"receiving {cat_name} chunk {count}")

                        try:
                            response = await asyncio.wait_for(stream.recv_message(), timeout=timeout)
                        except Exception as exc:
                            if 'Incomplete data' in str(exc):
                                raise UnexpectedEndOfStream(str(exc))

                            raise

                        if not response:
                            raise UnexpectedEndOfStream("No response")

                        raise_message_exception(response)

            finally:
                await write_queue.put(None)
                await write_task

            file_hash = await call_in_executor(get_file_hash, hash_code, path, executor=process_executor)  # type: ignore
            if hash_digest != file_hash:
                await logger.error(f"receiving {cat_name} failed: hash mismatch")
                raise AssetHashMismatchError("Hash value mismatch")

            await logger.debug(f"receiving {cat_name} done")

        return data, existing
