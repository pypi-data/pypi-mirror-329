from momotor.rpc.proto import exception_pb2 as _exception_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SharedLockRequest(_message.Message):
    __slots__ = ("lock", "key", "exclusive")
    LOCK_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    lock: bool
    key: str
    exclusive: bool
    def __init__(self, lock: bool = ..., key: _Optional[str] = ..., exclusive: bool = ...) -> None: ...

class SharedLockResponse(_message.Message):
    __slots__ = ("locked", "exception")
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    locked: bool
    exception: _exception_pb2.Exception
    def __init__(self, locked: bool = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
