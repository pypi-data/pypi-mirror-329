from momotor.rpc.proto import exception_pb2 as _exception_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateResourceAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_RESOURCE_ACTION: _ClassVar[UpdateResourceAction]
    ADD_RESOURCE_ACTION: _ClassVar[UpdateResourceAction]
    REMOVE_RESOURCE_ACTION: _ClassVar[UpdateResourceAction]
    SET_RESOURCE_ACTION: _ClassVar[UpdateResourceAction]
NO_RESOURCE_ACTION: UpdateResourceAction
ADD_RESOURCE_ACTION: UpdateResourceAction
REMOVE_RESOURCE_ACTION: UpdateResourceAction
SET_RESOURCE_ACTION: UpdateResourceAction

class Resource(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class UpdateResourceRequest(_message.Message):
    __slots__ = ("action", "resource")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    action: UpdateResourceAction
    resource: _containers.RepeatedCompositeFieldContainer[Resource]
    def __init__(self, action: _Optional[_Union[UpdateResourceAction, str]] = ..., resource: _Optional[_Iterable[_Union[Resource, _Mapping]]] = ...) -> None: ...

class UpdateResourceResponse(_message.Message):
    __slots__ = ("exception",)
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    exception: _exception_pb2.Exception
    def __init__(self, exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
