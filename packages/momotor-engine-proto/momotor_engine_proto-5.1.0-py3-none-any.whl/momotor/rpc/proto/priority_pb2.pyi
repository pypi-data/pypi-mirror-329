from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Priority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NORMAL: _ClassVar[Priority]
    LOWEST: _ClassVar[Priority]
    LOW: _ClassVar[Priority]
    HIGH: _ClassVar[Priority]
    HIGHEST: _ClassVar[Priority]
NORMAL: Priority
LOWEST: Priority
LOW: Priority
HIGH: Priority
HIGHEST: Priority
