from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MESSAGE_ACTION_TYPE_UNSPECIFIED: _ClassVar[MessageActionType]
    MESSAGE_ACTION_TYPE_URL: _ClassVar[MessageActionType]
    MESSAGE_ACTION_TYPE_CALLBACK: _ClassVar[MessageActionType]
    MESSAGE_ACTION_TYPE_CALLBACK_PARAMETRIZED: _ClassVar[MessageActionType]

class SentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SENT_STATUS_UNSPECIFIED: _ClassVar[SentStatus]
    SENT_STATUS_SENT: _ClassVar[SentStatus]
    SENT_STATUS_ERROR: _ClassVar[SentStatus]
    SENT_STATUS_USER_BLOCKED: _ClassVar[SentStatus]
MESSAGE_ACTION_TYPE_UNSPECIFIED: MessageActionType
MESSAGE_ACTION_TYPE_URL: MessageActionType
MESSAGE_ACTION_TYPE_CALLBACK: MessageActionType
MESSAGE_ACTION_TYPE_CALLBACK_PARAMETRIZED: MessageActionType
SENT_STATUS_UNSPECIFIED: SentStatus
SENT_STATUS_SENT: SentStatus
SENT_STATUS_ERROR: SentStatus
SENT_STATUS_USER_BLOCKED: SentStatus

class MessageAction(_message.Message):
    __slots__ = ["title", "url", "callback"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CALLBACK_FIELD_NUMBER: _ClassVar[int]
    title: str
    url: str
    callback: str
    def __init__(self, title: _Optional[str] = ..., url: _Optional[str] = ..., callback: _Optional[str] = ...) -> None: ...

class SendMessageRequest(_message.Message):
    __slots__ = ["message", "bot_id", "actions", "recipient_ids", "hook_tag", "is_silent", "metadata"]
    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_IDS_FIELD_NUMBER: _ClassVar[int]
    HOOK_TAG_FIELD_NUMBER: _ClassVar[int]
    IS_SILENT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    message: str
    bot_id: int
    actions: _containers.RepeatedCompositeFieldContainer[MessageAction]
    recipient_ids: _containers.RepeatedScalarFieldContainer[int]
    hook_tag: str
    is_silent: bool
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, message: _Optional[str] = ..., bot_id: _Optional[int] = ..., actions: _Optional[_Iterable[_Union[MessageAction, _Mapping]]] = ..., recipient_ids: _Optional[_Iterable[int]] = ..., hook_tag: _Optional[str] = ..., is_silent: bool = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TriggerHookRequest(_message.Message):
    __slots__ = ["hook_tag", "bot_id", "recipient_id", "metadata"]
    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    HOOK_TAG_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    hook_tag: str
    bot_id: int
    recipient_id: int
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, hook_tag: _Optional[str] = ..., bot_id: _Optional[int] = ..., recipient_id: _Optional[int] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MessageSentStatus(_message.Message):
    __slots__ = ["recipient_id", "status"]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    recipient_id: int
    status: SentStatus
    def __init__(self, recipient_id: _Optional[int] = ..., status: _Optional[_Union[SentStatus, str]] = ...) -> None: ...

class SendMessageResponse(_message.Message):
    __slots__ = ["statuses"]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    statuses: _containers.RepeatedCompositeFieldContainer[MessageSentStatus]
    def __init__(self, statuses: _Optional[_Iterable[_Union[MessageSentStatus, _Mapping]]] = ...) -> None: ...

class RefundRequest(_message.Message):
    __slots__ = ["bot_id", "recipient_id", "transaction_id", "refund_reason"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    REFUND_REASON_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    recipient_id: int
    transaction_id: str
    refund_reason: str
    def __init__(self, bot_id: _Optional[int] = ..., recipient_id: _Optional[int] = ..., transaction_id: _Optional[str] = ..., refund_reason: _Optional[str] = ...) -> None: ...
