from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DATA_TYPE_UNSPECIFIED: _ClassVar[DataType]
    DATA_TYPE_FULL_NAME: _ClassVar[DataType]
    DATA_TYPE_BIRTH_PLACE: _ClassVar[DataType]
    DATA_TYPE_BIRTH_DATE_TIME: _ClassVar[DataType]
DATA_TYPE_UNSPECIFIED: DataType
DATA_TYPE_FULL_NAME: DataType
DATA_TYPE_BIRTH_PLACE: DataType
DATA_TYPE_BIRTH_DATE_TIME: DataType

class ValidationRequest(_message.Message):
    __slots__ = ["type", "input", "extra_prompt", "language"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    EXTRA_PROMPT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    type: DataType
    input: str
    extra_prompt: str
    language: str
    def __init__(self, type: _Optional[_Union[DataType, str]] = ..., input: _Optional[str] = ..., extra_prompt: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class ValidationResponse(_message.Message):
    __slots__ = ["is_valid", "unified_result", "error_message"]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    UNIFIED_RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    unified_result: str
    error_message: str
    def __init__(self, is_valid: bool = ..., unified_result: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class ValidateSpreadQuestionRequest(_message.Message):
    __slots__ = ["input", "question_category", "language"]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    QUESTION_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    input: str
    question_category: str
    language: str
    def __init__(self, input: _Optional[str] = ..., question_category: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...
