from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MESSAGE_DIRECTION_UNSPECIFIED: _ClassVar[MessageDirection]
    MESSAGE_DIRECTION_CUSTOMER: _ClassVar[MessageDirection]
    MESSAGE_DIRECTION_BOT: _ClassVar[MessageDirection]
    MESSAGE_DIRECTION_ADMIN: _ClassVar[MessageDirection]
MESSAGE_DIRECTION_UNSPECIFIED: MessageDirection
MESSAGE_DIRECTION_CUSTOMER: MessageDirection
MESSAGE_DIRECTION_BOT: MessageDirection
MESSAGE_DIRECTION_ADMIN: MessageDirection

class SaveMessageRequest(_message.Message):
    __slots__ = ["chat_id", "bot_id", "content", "direction", "attachments", "date_time", "message_id"]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: int
    bot_id: int
    content: str
    direction: MessageDirection
    attachments: str
    date_time: str
    message_id: int
    def __init__(self, chat_id: _Optional[int] = ..., bot_id: _Optional[int] = ..., content: _Optional[str] = ..., direction: _Optional[_Union[MessageDirection, str]] = ..., attachments: _Optional[str] = ..., date_time: _Optional[str] = ..., message_id: _Optional[int] = ...) -> None: ...

class SaveMessageResponse(_message.Message):
    __slots__ = ["internal_id"]
    INTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    internal_id: str
    def __init__(self, internal_id: _Optional[str] = ...) -> None: ...
