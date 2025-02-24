from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ToolSet(_message.Message):
    __slots__ = ("tool",)
    TOOL_FIELD_NUMBER: _ClassVar[int]
    tool: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, tool: _Optional[_Iterable[str]] = ...) -> None: ...
