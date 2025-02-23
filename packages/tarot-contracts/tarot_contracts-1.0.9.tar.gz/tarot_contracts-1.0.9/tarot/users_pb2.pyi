from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TRANSACTION_TYPE_UNSPECIFIED: _ClassVar[TransactionType]
    TRANSACTION_TYPE_INCOME: _ClassVar[TransactionType]
    TRANSACTION_TYPE_OUTCOME: _ClassVar[TransactionType]

class TransactionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TRANSACTION_STATUS_UNSPECIFIED: _ClassVar[TransactionStatus]
    TRANSACTION_STATUS_SUCCESS: _ClassVar[TransactionStatus]
    TRANSACTION_STATUS_PENDING: _ClassVar[TransactionStatus]
    TRANSACTION_STATUS_FAILED: _ClassVar[TransactionStatus]
TRANSACTION_TYPE_UNSPECIFIED: TransactionType
TRANSACTION_TYPE_INCOME: TransactionType
TRANSACTION_TYPE_OUTCOME: TransactionType
TRANSACTION_STATUS_UNSPECIFIED: TransactionStatus
TRANSACTION_STATUS_SUCCESS: TransactionStatus
TRANSACTION_STATUS_PENDING: TransactionStatus
TRANSACTION_STATUS_FAILED: TransactionStatus

class TelegramUser(_message.Message):
    __slots__ = ["id", "username", "first_name", "last_name", "language_code", "is_bot", "is_premium", "profile_photos", "customer_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    IS_BOT_FIELD_NUMBER: _ClassVar[int]
    IS_PREMIUM_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PHOTOS_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    username: str
    first_name: str
    last_name: str
    language_code: str
    is_bot: bool
    is_premium: bool
    profile_photos: _containers.RepeatedScalarFieldContainer[str]
    customer_id: str
    def __init__(self, id: _Optional[int] = ..., username: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., language_code: _Optional[str] = ..., is_bot: bool = ..., is_premium: bool = ..., profile_photos: _Optional[_Iterable[str]] = ..., customer_id: _Optional[str] = ...) -> None: ...

class CreateTelegramUserRequest(_message.Message):
    __slots__ = ["tg_user", "bot_id"]
    TG_USER_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    tg_user: TelegramUser
    bot_id: int
    def __init__(self, tg_user: _Optional[_Union[TelegramUser, _Mapping]] = ..., bot_id: _Optional[int] = ...) -> None: ...

class SpreadProfile(_message.Message):
    __slots__ = ["tg_id", "bot_id", "full_name", "birth_date", "birth_place", "zodiac_sign", "chinese_zodiac_sign", "gender"]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    BIRTH_DATE_FIELD_NUMBER: _ClassVar[int]
    BIRTH_PLACE_FIELD_NUMBER: _ClassVar[int]
    ZODIAC_SIGN_FIELD_NUMBER: _ClassVar[int]
    CHINESE_ZODIAC_SIGN_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    tg_id: int
    bot_id: int
    full_name: str
    birth_date: str
    birth_place: str
    zodiac_sign: str
    chinese_zodiac_sign: str
    gender: str
    def __init__(self, tg_id: _Optional[int] = ..., bot_id: _Optional[int] = ..., full_name: _Optional[str] = ..., birth_date: _Optional[str] = ..., birth_place: _Optional[str] = ..., zodiac_sign: _Optional[str] = ..., chinese_zodiac_sign: _Optional[str] = ..., gender: _Optional[str] = ...) -> None: ...

class GetCustomerRequest(_message.Message):
    __slots__ = ["customer_id", "tg_id", "bot_id"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    tg_id: int
    bot_id: int
    def __init__(self, customer_id: _Optional[str] = ..., tg_id: _Optional[int] = ..., bot_id: _Optional[int] = ...) -> None: ...

class CreateCustomerRequest(_message.Message):
    __slots__ = ["tg_user", "bot_id"]
    TG_USER_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    tg_user: TelegramUser
    bot_id: int
    def __init__(self, tg_user: _Optional[_Union[TelegramUser, _Mapping]] = ..., bot_id: _Optional[int] = ...) -> None: ...

class CustomerLanguageRequest(_message.Message):
    __slots__ = ["language", "customer_id", "tg_id", "bot_id"]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    language: str
    customer_id: str
    tg_id: int
    bot_id: int
    def __init__(self, language: _Optional[str] = ..., customer_id: _Optional[str] = ..., tg_id: _Optional[int] = ..., bot_id: _Optional[int] = ...) -> None: ...

class CustomerProfile(_message.Message):
    __slots__ = ["id", "tg_user", "spread_profile", "actual_balance", "language", "referral_id", "bot_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TG_USER_FIELD_NUMBER: _ClassVar[int]
    SPREAD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_BALANCE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    REFERRAL_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    tg_user: TelegramUser
    spread_profile: SpreadProfile
    actual_balance: int
    language: str
    referral_id: str
    bot_id: int
    def __init__(self, id: _Optional[str] = ..., tg_user: _Optional[_Union[TelegramUser, _Mapping]] = ..., spread_profile: _Optional[_Union[SpreadProfile, _Mapping]] = ..., actual_balance: _Optional[int] = ..., language: _Optional[str] = ..., referral_id: _Optional[str] = ..., bot_id: _Optional[int] = ...) -> None: ...

class CustomerBalance(_message.Message):
    __slots__ = ["id", "actual_balance"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_BALANCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    actual_balance: int
    def __init__(self, id: _Optional[str] = ..., actual_balance: _Optional[int] = ...) -> None: ...

class CustomerTransaction(_message.Message):
    __slots__ = ["id", "customer_id", "type", "amount", "price", "currency", "description", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    customer_id: str
    type: TransactionType
    amount: int
    price: int
    currency: str
    description: str
    created_at: str
    def __init__(self, id: _Optional[str] = ..., customer_id: _Optional[str] = ..., type: _Optional[_Union[TransactionType, str]] = ..., amount: _Optional[int] = ..., price: _Optional[int] = ..., currency: _Optional[str] = ..., description: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class CustomerTransactions(_message.Message):
    __slots__ = ["transactions"]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[CustomerTransaction]
    def __init__(self, transactions: _Optional[_Iterable[_Union[CustomerTransaction, _Mapping]]] = ...) -> None: ...

class TopUpBalanceRequest(_message.Message):
    __slots__ = ["customer_id", "tg_id", "bot_id", "amount", "price", "currency", "payment_provider_transaction_id"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_PROVIDER_TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    tg_id: int
    bot_id: int
    amount: int
    price: int
    currency: str
    payment_provider_transaction_id: str
    def __init__(self, customer_id: _Optional[str] = ..., tg_id: _Optional[int] = ..., bot_id: _Optional[int] = ..., amount: _Optional[int] = ..., price: _Optional[int] = ..., currency: _Optional[str] = ..., payment_provider_transaction_id: _Optional[str] = ...) -> None: ...

class InternalPurchaseRequest(_message.Message):
    __slots__ = ["customer_id", "tg_id", "bot_id"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    TG_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_ID_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    tg_id: int
    bot_id: int
    def __init__(self, customer_id: _Optional[str] = ..., tg_id: _Optional[int] = ..., bot_id: _Optional[int] = ...) -> None: ...

class CommitInternalPurchaseRequest(_message.Message):
    __slots__ = ["transaction_id"]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    transaction_id: str
    def __init__(self, transaction_id: _Optional[str] = ...) -> None: ...

class RegisterReferralRequest(_message.Message):
    __slots__ = ["customer_id", "referrer_id"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    REFERRER_ID_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    referrer_id: str
    def __init__(self, customer_id: _Optional[str] = ..., referrer_id: _Optional[str] = ...) -> None: ...
