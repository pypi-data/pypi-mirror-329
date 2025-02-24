from momotor.rpc.proto import asset_pb2 as _asset_pb2
from momotor.rpc.proto import exception_pb2 as _exception_pb2
from momotor.rpc.proto import shared_pb2 as _shared_pb2
from momotor.rpc.proto import task_pb2 as _task_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateTaskStatusRequest(_message.Message):
    __slots__ = ("taskId", "progress")
    TASKID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    taskId: _task_pb2.TaskId
    progress: float
    def __init__(self, taskId: _Optional[_Union[_task_pb2.TaskId, _Mapping]] = ..., progress: _Optional[float] = ...) -> None: ...

class UpdateTaskStatusResponse(_message.Message):
    __slots__ = ("exception",)
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    exception: _exception_pb2.Exception
    def __init__(self, exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
