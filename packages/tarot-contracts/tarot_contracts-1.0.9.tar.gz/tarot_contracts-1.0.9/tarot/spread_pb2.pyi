from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MESSAGE_ROLE_UNSPECIFIED: _ClassVar[MessageRole]
    MESSAGE_ROLE_SYSTEM: _ClassVar[MessageRole]
    MESSAGE_ROLE_HUMAN: _ClassVar[MessageRole]
    MESSAGE_ROLE_AI: _ClassVar[MessageRole]
MESSAGE_ROLE_UNSPECIFIED: MessageRole
MESSAGE_ROLE_SYSTEM: MessageRole
MESSAGE_ROLE_HUMAN: MessageRole
MESSAGE_ROLE_AI: MessageRole

class TarotSpreadRequest(_message.Message):
    __slots__ = ["question", "category", "bot_id", "tg_id", "language"]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    question: str
    category: str
    bot_id: int
    tg_id: int
    language: str
    def __init__(self, question: _Optional[str] = ..., category: _Optional[str] = ..., bot_id: _Optional[int] = ..., tg_id: _Optional[int] = ..., language: _Optional[str] = ...) -> None: ...

class TarotShortSpreadRequest(_message.Message):
    __slots__ = ["bot_id", "tg_id", "language"]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    bot_id: int
    tg_id: int
    language: str
    def __init__(self, bot_id: _Optional[int] = ..., tg_id: _Optional[int] = ..., language: _Optional[str] = ...) -> None: ...

class TarotShortSpreadResponse(_message.Message):
    __slots__ = ["spread"]
    SPREAD_FIELD_NUMBER: _ClassVar[int]
    spread: str
    def __init__(self, spread: _Optional[str] = ...) -> None: ...

class TarotSpreadResponse(_message.Message):
    __slots__ = ["question", "category", "spread"]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FIELD_NUMBER: _ClassVar[int]
    question: str
    category: str
    spread: str
    def __init__(self, question: _Optional[str] = ..., category: _Optional[str] = ..., spread: _Optional[str] = ...) -> None: ...

class SpreadHistoryItem(_message.Message):
    __slots__ = ["content", "role", "timestamp"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    content: str
    role: MessageRole
    timestamp: str
    def __init__(self, content: _Optional[str] = ..., role: _Optional[_Union[MessageRole, str]] = ..., timestamp: _Optional[str] = ...) -> None: ...

class SaveSpreadRequest(_message.Message):
    __slots__ = ["tg_id", "bot_id", "spread", "question", "category", "transport_task_id", "language", "histories"]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    HISTORIES_FIELD_NUMBER: _ClassVar[int]
    tg_id: int
    bot_id: int
    spread: str
    question: str
    category: str
    transport_task_id: str
    language: str
    histories: _containers.RepeatedCompositeFieldContainer[SpreadHistoryItem]
    def __init__(self, tg_id: _Optional[int] = ..., bot_id: _Optional[int] = ..., spread: _Optional[str] = ..., question: _Optional[str] = ..., category: _Optional[str] = ..., transport_task_id: _Optional[str] = ..., language: _Optional[str] = ..., histories: _Optional[_Iterable[_Union[SpreadHistoryItem, _Mapping]]] = ...) -> None: ...

class AdditionalQuestionRequest(_message.Message):
    __slots__ = ["question", "spread_id", "bot_id", "tg_id", "language"]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    SPREAD_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    question: str
    spread_id: str
    bot_id: int
    tg_id: int
    language: str
    def __init__(self, question: _Optional[str] = ..., spread_id: _Optional[str] = ..., bot_id: _Optional[int] = ..., tg_id: _Optional[int] = ..., language: _Optional[str] = ...) -> None: ...

class AdditionalQuestionResponse(_message.Message):
    __slots__ = ["spread_id", "question", "answer"]
    SPREAD_ID_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    spread_id: str
    question: str
    answer: str
    def __init__(self, spread_id: _Optional[str] = ..., question: _Optional[str] = ..., answer: _Optional[str] = ...) -> None: ...
