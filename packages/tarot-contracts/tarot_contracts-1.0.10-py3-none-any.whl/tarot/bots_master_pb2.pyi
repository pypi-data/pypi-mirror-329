from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BotGroup(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    BOT_GROUP_UNSPECIFIED: _ClassVar[BotGroup]
    BOT_GROUP_TAROT: _ClassVar[BotGroup]

class BotProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    BOT_PROVIDER_UNSPECIFIED: _ClassVar[BotProvider]
    BOT_PROVIDER_TELEGRAM: _ClassVar[BotProvider]
    BOT_PROVIDER_SLACK: _ClassVar[BotProvider]
    BOT_PROVIDER_VIBER: _ClassVar[BotProvider]
BOT_GROUP_UNSPECIFIED: BotGroup
BOT_GROUP_TAROT: BotGroup
BOT_PROVIDER_UNSPECIFIED: BotProvider
BOT_PROVIDER_TELEGRAM: BotProvider
BOT_PROVIDER_SLACK: BotProvider
BOT_PROVIDER_VIBER: BotProvider

class PricingPlan(_message.Message):
    __slots__ = ["id", "name", "description", "price", "credits"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CREDITS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    price: int
    credits: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., price: _Optional[int] = ..., credits: _Optional[int] = ...) -> None: ...

class RetentionConfig(_message.Message):
    __slots__ = ["enabled", "frequency", "prompt", "bot_hook"]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    BOT_HOOK_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    frequency: str
    prompt: str
    bot_hook: str
    def __init__(self, enabled: bool = ..., frequency: _Optional[str] = ..., prompt: _Optional[str] = ..., bot_hook: _Optional[str] = ...) -> None: ...

class TarotBotConfig(_message.Message):
    __slots__ = ["spread_prompt", "pricing_plans", "default_language"]
    SPREAD_PROMPT_FIELD_NUMBER: _ClassVar[int]
    PRICING_PLANS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    spread_prompt: str
    pricing_plans: _containers.RepeatedCompositeFieldContainer[PricingPlan]
    default_language: str
    def __init__(self, spread_prompt: _Optional[str] = ..., pricing_plans: _Optional[_Iterable[_Union[PricingPlan, _Mapping]]] = ..., default_language: _Optional[str] = ...) -> None: ...

class Bot(_message.Message):
    __slots__ = ["id", "token", "group", "provider", "name", "tarot_config", "retention_config"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAROT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RETENTION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: int
    token: str
    group: BotGroup
    provider: BotProvider
    name: str
    tarot_config: TarotBotConfig
    retention_config: RetentionConfig
    def __init__(self, id: _Optional[int] = ..., token: _Optional[str] = ..., group: _Optional[_Union[BotGroup, str]] = ..., provider: _Optional[_Union[BotProvider, str]] = ..., name: _Optional[str] = ..., tarot_config: _Optional[_Union[TarotBotConfig, _Mapping]] = ..., retention_config: _Optional[_Union[RetentionConfig, _Mapping]] = ...) -> None: ...

class RetrieveBotsRequest(_message.Message):
    __slots__ = ["group", "provider"]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    group: BotGroup
    provider: BotProvider
    def __init__(self, group: _Optional[_Union[BotGroup, str]] = ..., provider: _Optional[_Union[BotProvider, str]] = ...) -> None: ...

class RetrieveBotsResponse(_message.Message):
    __slots__ = ["bots"]
    BOTS_FIELD_NUMBER: _ClassVar[int]
    bots: _containers.RepeatedCompositeFieldContainer[Bot]
    def __init__(self, bots: _Optional[_Iterable[_Union[Bot, _Mapping]]] = ...) -> None: ...

class RetrieveBotRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
