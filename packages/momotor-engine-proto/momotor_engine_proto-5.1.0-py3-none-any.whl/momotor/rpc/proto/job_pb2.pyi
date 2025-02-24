from google.protobuf import duration_pb2 as _duration_pb2
from momotor.rpc.proto import exception_pb2 as _exception_pb2
from momotor.rpc.proto import priority_pb2 as _priority_pb2
from momotor.rpc.proto import resource_pb2 as _resource_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_JOB_TYPE: _ClassVar[JobType]
    TEST_RECIPE: _ClassVar[JobType]
    VERIFY_PRODUCT: _ClassVar[JobType]

class JobState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_JOB_STATE: _ClassVar[JobState]
    INITIALIZING: _ClassVar[JobState]
    QUEUED: _ClassVar[JobState]
    STARTED: _ClassVar[JobState]
    FINISHED: _ClassVar[JobState]
    CANCELLED: _ClassVar[JobState]
    FAILED: _ClassVar[JobState]
NO_JOB_TYPE: JobType
TEST_RECIPE: JobType
VERIFY_PRODUCT: JobType
NO_JOB_STATE: JobState
INITIALIZING: JobState
QUEUED: JobState
STARTED: JobState
FINISHED: JobState
CANCELLED: JobState
FAILED: JobState

class JobStatus(_message.Message):
    __slots__ = ("state", "time", "tasks", "tasksActive", "tasksFinished", "failure", "priority")
    STATE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    TASKSACTIVE_FIELD_NUMBER: _ClassVar[int]
    TASKSFINISHED_FIELD_NUMBER: _ClassVar[int]
    FAILURE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    state: JobState
    time: _duration_pb2.Duration
    tasks: int
    tasksActive: int
    tasksFinished: int
    failure: str
    priority: _priority_pb2.Priority
    def __init__(self, state: _Optional[_Union[JobState, str]] = ..., time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., tasks: _Optional[int] = ..., tasksActive: _Optional[int] = ..., tasksFinished: _Optional[int] = ..., failure: _Optional[str] = ..., priority: _Optional[_Union[_priority_pb2.Priority, str]] = ...) -> None: ...

class CreateJobRequest(_message.Message):
    __slots__ = ("type", "noCache", "resource", "priority")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NOCACHE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    type: JobType
    noCache: bool
    resource: _containers.RepeatedCompositeFieldContainer[_resource_pb2.Resource]
    priority: _priority_pb2.Priority
    def __init__(self, type: _Optional[_Union[JobType, str]] = ..., noCache: bool = ..., resource: _Optional[_Iterable[_Union[_resource_pb2.Resource, _Mapping]]] = ..., priority: _Optional[_Union[_priority_pb2.Priority, str]] = ...) -> None: ...

class CreateJobResponse(_message.Message):
    __slots__ = ("jobId", "exception")
    JOBID_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    exception: _exception_pb2.Exception
    def __init__(self, jobId: _Optional[str] = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...

class StartJobRequest(_message.Message):
    __slots__ = ("jobId",)
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class StartJobResponse(_message.Message):
    __slots__ = ("exception",)
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    exception: _exception_pb2.Exception
    def __init__(self, exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...

class JobStatusRequest(_message.Message):
    __slots__ = ("jobId",)
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class JobStatusResponse(_message.Message):
    __slots__ = ("status", "exception")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    status: JobStatus
    exception: _exception_pb2.Exception
    def __init__(self, status: _Optional[_Union[JobStatus, _Mapping]] = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...

class EndJobRequest(_message.Message):
    __slots__ = ("jobId",)
    JOBID_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    def __init__(self, jobId: _Optional[str] = ...) -> None: ...

class EndJobResponse(_message.Message):
    __slots__ = ("exception",)
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    exception: _exception_pb2.Exception
    def __init__(self, exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...

class JobStatusStream(_message.Message):
    __slots__ = ("jobId", "status", "exception")
    JOBID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    jobId: str
    status: JobStatus
    exception: _exception_pb2.Exception
    def __init__(self, jobId: _Optional[str] = ..., status: _Optional[_Union[JobStatus, _Mapping]] = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
