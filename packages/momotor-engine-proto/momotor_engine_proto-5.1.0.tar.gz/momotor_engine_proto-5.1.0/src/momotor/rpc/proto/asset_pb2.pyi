from momotor.rpc.proto import exception_pb2 as _exception_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_CATEGORY: _ClassVar[Category]
    RECIPE: _ClassVar[Category]
    CONFIG: _ClassVar[Category]
    PRODUCT: _ClassVar[Category]
    RESULT: _ClassVar[Category]

class AssetFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_ASSET_FORMAT: _ClassVar[AssetFormat]
    XML: _ClassVar[AssetFormat]
    ZIP: _ClassVar[AssetFormat]
NO_CATEGORY: Category
RECIPE: Category
CONFIG: Category
PRODUCT: Category
RESULT: Category
NO_ASSET_FORMAT: AssetFormat
XML: AssetFormat
ZIP: AssetFormat

class AssetQuery(_message.Message):
    __slots__ = ("category", "testId", "stepId", "taskNumber")
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TESTID_FIELD_NUMBER: _ClassVar[int]
    STEPID_FIELD_NUMBER: _ClassVar[int]
    TASKNUMBER_FIELD_NUMBER: _ClassVar[int]
    category: Category
    testId: str
    stepId: str
    taskNumber: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, category: _Optional[_Union[Category, str]] = ..., testId: _Optional[str] = ..., stepId: _Optional[str] = ..., taskNumber: _Optional[_Iterable[int]] = ...) -> None: ...

class AssetData(_message.Message):
    __slots__ = ("query", "name", "format", "size", "hash")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    query: AssetQuery
    name: str
    format: AssetFormat
    size: int
    hash: bytes
    def __init__(self, query: _Optional[_Union[AssetQuery, _Mapping]] = ..., name: _Optional[str] = ..., format: _Optional[_Union[AssetFormat, str]] = ..., size: _Optional[int] = ..., hash: _Optional[bytes] = ...) -> None: ...

class UploadAssetRequest(_message.Message):
    __slots__ = ("jobId", "assetData", "chunk")
    JOBID_FIELD_NUMBER: _ClassVar[int]
    ASSETDATA_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    assetData: AssetData
    chunk: bytes
    def __init__(self, jobId: _Optional[str] = ..., assetData: _Optional[_Union[AssetData, _Mapping]] = ..., chunk: _Optional[bytes] = ...) -> None: ...

class UploadAssetResponse(_message.Message):
    __slots__ = ("assetSelected", "exception")
    ASSETSELECTED_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    assetSelected: bool
    exception: _exception_pb2.Exception
    def __init__(self, assetSelected: bool = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...

class DownloadAssetRequest(_message.Message):
    __slots__ = ("jobId", "query", "accepted")
    JOBID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    query: AssetQuery
    accepted: bool
    def __init__(self, jobId: _Optional[str] = ..., query: _Optional[_Union[AssetQuery, _Mapping]] = ..., accepted: bool = ...) -> None: ...

class DownloadAssetResponse(_message.Message):
    __slots__ = ("data", "chunk", "exception")
    DATA_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    data: AssetData
    chunk: bytes
    exception: _exception_pb2.Exception
    def __init__(self, data: _Optional[_Union[AssetData, _Mapping]] = ..., chunk: _Optional[bytes] = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
