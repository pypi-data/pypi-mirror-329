from __future__ import annotations

import typing

from grpclib.client import Channel, Stream
from grpclib.config import Configuration
from grpclib.const import Cardinality
from grpclib.metadata import Deadline, _Metadata, _MetadataLike
from grpclib.stream import _RecvType, _SendType
from momotor.shared.doc import annotate_docstring
from momotor.shared.log import getAsyncLogger
from multidict import MultiDict

from momotor.rpc.auth.utils import calculate_challenge_response
from momotor.rpc.exception import RPCException, raise_message_exception
from momotor.rpc.proto.auth_grpc import AuthStub
from momotor.rpc.proto.auth_pb2 import AuthenticateRequest, \
    AuthenticateResponse, Challenge
from momotor.rpc.utils import setup_h2_logging
from momotor.rpc.validate.response import validate_authenticate_response

logger = getAsyncLogger(__package__)

DEFAULT_PORT = 50051
DEFAULT_SSL_PORT = 50052


if typing.TYPE_CHECKING:
    base = Channel
else:
    base = object


class AuthenticatingChannel(base):
    """ Wrapper for :py:class:`grpclib.client.Channel` that adds an `auth-token` metadata to any request.

    Proxies all methods of :py:class:`grpclib.client.Channel`, and adds a few additional methods
    """
    def __init__(self, channel: Channel, auth_token=None):
        self._channel = channel
        self.auth_token = auth_token

    def is_authenticated(self) -> bool:
        """ Returns `True` if an auth-token is set """
        return self.auth_token is not None

    def request(
            self,
            name: str,
            cardinality: Cardinality,
            request_type: type[_SendType],
            reply_type: type[_RecvType],
            *,
            timeout: float | None = None,
            deadline: Deadline | None = None,
            metadata: _MetadataLike | None = None
    ) -> Stream[_SendType, _RecvType]:
        """ Wrapper for :py:func:`grpclib.client.Channel.request`
        """
        auth_metadata = typing.cast(_Metadata, MultiDict(metadata or ()))
        if self.auth_token:
            auth_metadata['auth-token'] = self.auth_token
        if metadata is not None:
            auth_metadata.update(metadata)

        return self._channel.request(
            name, cardinality, request_type, reply_type,
            timeout=timeout, deadline=deadline, metadata=auth_metadata
        )

    def __getattr__(self, name):
        attr = getattr(self._channel, name)
        setattr(self, name, attr)
        return attr


async def authenticate(channel: Channel, api_key: str, api_secret: str, *, stub: AuthStub | None = None) \
        -> AuthenticatingChannel:
    """ Authenticate with the server. Returns an :py:class:`AuthenticatingChannel`.

    Any exception returned by the server is raised as a subclass of `RPCException`

    :param channel: channel to authenticate with
    :param api_key: Client's api-key
    :param api_secret: Client's api-secret
    :param stub: stub to authenticate with (defaults to `AuthStub(channel)`)
    """
    channel = AuthenticatingChannel(channel)

    if not stub:
        stub = AuthStub(channel)

    async with stub.authenticate.open() as auth_stream:
        await auth_stream.send_message(AuthenticateRequest(apiKey=api_key))

        response: AuthenticateResponse | None = await auth_stream.recv_message()
        raise_message_exception(response)
        assert response is not None
        validate_authenticate_response(response, expect_oneof='challenge')

        challenge: Challenge = response.challenge
        challenge_response = calculate_challenge_response(api_key, api_secret, challenge.salt, challenge.value)

        await auth_stream.send_message(AuthenticateRequest(challengeResponse=challenge_response), end=True)

        response = await auth_stream.recv_message()
        raise_message_exception(response)
        assert response is not None
        validate_authenticate_response(response, expect_oneof='authToken')

        channel.auth_token = response.authToken

    return channel


@annotate_docstring(logger=logger)
async def get_authenticated_channel(host: str, port: int | None,
                                    api_key: str, api_secret: str, auth_token: str | None = None,
                                    *, ssl_context=None, loop=None, log_h2=False,
                                    keepalive_time=900,
                                    **channel_opts) \
        -> tuple[AuthenticatingChannel, AuthStub]:
    """ Connect to a broker and authenticate, possibly using an already existing token.

    Returns a tuple with

    * the authenticated channel
    * the auth stub

    If authentication fails, raises (a subclass of) :py:class:`~momotor.rpc.exception.RPCException`

    Produces logging information on the ``{logger.name}`` logger

    :param host: Broker's hostname
    :param port: Broker's port. If None, uses default ports 50051 or 50052, depending on ssl_context value
    :param api_key: API key to authenticate with
    :param api_secret: API secret to authenticate with
    :param auth_token: (optional) existing authentication token to reuse session
    :param ssl_context: SSL context to use
    :param loop: asyncio event loop (Deprecated)
    :param log_h2: if True, enables logging of the h2 library
    :param keepalive_time: keep alive time (None to disable)
    :param channel_opts: additional keyword arguments supplied to `grpclib.channel.Channel`
    :return: tuple containing: the authenticated channel and the auth stub
    """
    if ssl_context:
        import ssl
        ssl_info = f' (using {ssl.OPENSSL_VERSION})'
    else:
        ssl_info = ' (without SSL)'

    if port is None:
        port = DEFAULT_PORT if ssl_context is None else DEFAULT_SSL_PORT

    await logger.debug(f'creating channel to {host} on {port}{ssl_info}')
    config = Configuration(
        _keepalive_time=keepalive_time,
        _http2_max_pings_without_data=0,
        _http2_min_sent_ping_interval_without_data=1,
    )
    channel = Channel(host=host, port=port, ssl=ssl_context, config=config, **channel_opts, loop=loop)

    if log_h2:
        setup_h2_logging(channel)

    if auth_token:
        await logger.debug("attempting to re-use existing auth-token")

        auth_channel = AuthenticatingChannel(channel, auth_token)
        auth_stub = AuthStub(channel)

    else:
        try:
            auth_stub = AuthStub(channel)

            await logger.info(f"authenticating with api-key {api_key}")
            auth_channel = await authenticate(
                channel,
                api_key=api_key,
                api_secret=api_secret,
                stub=auth_stub,
            )

        except RPCException as exc:
            await logger.critical("broker authentication failed: %s", exc)
            try:
                channel.close()
            except:
                pass

            raise

        else:
            await logger.info("authenticated with new auth-token")

    return auth_channel, auth_stub


__all__ = ['AuthenticatingChannel', 'authenticate', 'get_authenticated_channel', 'DEFAULT_PORT', 'DEFAULT_SSL_PORT']
