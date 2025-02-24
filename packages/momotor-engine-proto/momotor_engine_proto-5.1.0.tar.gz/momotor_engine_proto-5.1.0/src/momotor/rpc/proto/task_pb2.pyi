from momotor.rpc.proto import exception_pb2 as _exception_pb2
from momotor.rpc.proto import priority_pb2 as _priority_pb2
from momotor.rpc.proto import resource_pb2 as _resource_pb2
from momotor.rpc.proto import tool_pb2 as _tool_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskId(_message.Message):
    __slots__ = ("jobId", "stepId", "testId", "taskNumber")
    JOBID_FIELD_NUMBER: _ClassVar[int]
    STEPID_FIELD_NUMBER: _ClassVar[int]
    TESTID_FIELD_NUMBER: _ClassVar[int]
    TASKNUMBER_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    stepId: str
    testId: str
    taskNumber: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, jobId: _Optional[str] = ..., stepId: _Optional[str] = ..., testId: _Optional[str] = ..., taskNumber: _Optional[_Iterable[int]] = ...) -> None: ...

class GetTaskRequest(_message.Message):
    __slots__ = ("version", "resource", "tool", "rank")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    TOOL_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    version: str
    resource: _containers.RepeatedCompositeFieldContainer[_resource_pb2.Resource]
    tool: _containers.RepeatedCompositeFieldContainer[_tool_pb2.ToolSet]
    rank: int
    def __init__(self, version: _Optional[str] = ..., resource: _Optional[_Iterable[_Union[_resource_pb2.Resource, _Mapping]]] = ..., tool: _Optional[_Iterable[_Union[_tool_pb2.ToolSet, _Mapping]]] = ..., rank: _Optional[int] = ...) -> None: ...

class GetTaskResponse(_message.Message):
    __slots__ = ("taskId", "resource", "priority", "exception")
    TASKID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    taskId: TaskId
    resource: _containers.RepeatedCompositeFieldContainer[_resource_pb2.Resource]
    priority: _priority_pb2.Priority
    exception: _exception_pb2.Exception
    def __init__(self, taskId: _Optional[_Union[TaskId, _Mapping]] = ..., resource: _Optional[_Iterable[_Union[_resource_pb2.Resource, _Mapping]]] = ..., priority: _Optional[_Union[_priority_pb2.Priority, str]] = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
