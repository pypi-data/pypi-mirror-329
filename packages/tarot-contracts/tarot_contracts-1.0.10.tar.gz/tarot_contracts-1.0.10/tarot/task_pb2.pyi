from tarot import bot_pb2 as _bot_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TASK_STATUS_UNSPECIFIED: _ClassVar[TaskStatus]
    TASK_STATUS_PENDING: _ClassVar[TaskStatus]
    TASK_STATUS_IN_PROGRESS: _ClassVar[TaskStatus]
    TASK_STATUS_COMPLETED: _ClassVar[TaskStatus]
    TASK_STATUS_FAILED: _ClassVar[TaskStatus]

class TaskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TASK_TYPE_UNSPECIFIED: _ClassVar[TaskType]
    TASK_TYPE_SEND_MESSAGE: _ClassVar[TaskType]
    TASK_TYPE_SEND_BATCH_MESSAGE: _ClassVar[TaskType]
    TASK_TYPE_TRIGGER_HOOK: _ClassVar[TaskType]
TASK_STATUS_UNSPECIFIED: TaskStatus
TASK_STATUS_PENDING: TaskStatus
TASK_STATUS_IN_PROGRESS: TaskStatus
TASK_STATUS_COMPLETED: TaskStatus
TASK_STATUS_FAILED: TaskStatus
TASK_TYPE_UNSPECIFIED: TaskType
TASK_TYPE_SEND_MESSAGE: TaskType
TASK_TYPE_SEND_BATCH_MESSAGE: TaskType
TASK_TYPE_TRIGGER_HOOK: TaskType

class ScheduleTaskRequest(_message.Message):
    __slots__ = ["name", "type", "send_message", "trigger_hook", "due_timestamp"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SEND_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_HOOK_FIELD_NUMBER: _ClassVar[int]
    DUE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: TaskType
    send_message: _bot_pb2.SendMessageRequest
    trigger_hook: _bot_pb2.TriggerHookRequest
    due_timestamp: int
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[TaskType, str]] = ..., send_message: _Optional[_Union[_bot_pb2.SendMessageRequest, _Mapping]] = ..., trigger_hook: _Optional[_Union[_bot_pb2.TriggerHookRequest, _Mapping]] = ..., due_timestamp: _Optional[int] = ...) -> None: ...

class ScheduleTaskResponse(_message.Message):
    __slots__ = ["id", "name", "due_date", "type", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    due_date: str
    type: TaskType
    status: TaskStatus
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., due_date: _Optional[str] = ..., type: _Optional[_Union[TaskType, str]] = ..., status: _Optional[_Union[TaskStatus, str]] = ...) -> None: ...
