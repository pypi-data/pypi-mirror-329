from momotor.rpc.proto import exception_pb2 as _exception_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatisticsResponse(_message.Message):
    __slots__ = ("stats", "exception")
    STATS_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    stats: str
    exception: _exception_pb2.Exception
    def __init__(self, stats: _Optional[str] = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
