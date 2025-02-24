from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExceptionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_EXCEPTION: _ClassVar[ExceptionType]
    FORMAT: _ClassVar[ExceptionType]
    AUTH: _ClassVar[ExceptionType]
    JOB: _ClassVar[ExceptionType]
    ASSET: _ClassVar[ExceptionType]
    ASSET_NOT_FOUND: _ClassVar[ExceptionType]
INVALID_EXCEPTION: ExceptionType
FORMAT: ExceptionType
AUTH: ExceptionType
JOB: ExceptionType
ASSET: ExceptionType
ASSET_NOT_FOUND: ExceptionType

class Exception(_message.Message):
    __slots__ = ("type", "text")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    type: ExceptionType
    text: str
    def __init__(self, type: _Optional[_Union[ExceptionType, str]] = ..., text: _Optional[str] = ...) -> None: ...
