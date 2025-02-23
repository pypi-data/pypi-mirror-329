from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    APPLICATION_RESULT_NOT_AVAILABLE: _ClassVar[ApplicationResult]
    APPLICATION_RESULT_ACCEPTED: _ClassVar[ApplicationResult]
    APPLICATION_RESULT_REJECTED: _ClassVar[ApplicationResult]
    APPLICATION_RESULT_RECLAIMED: _ClassVar[ApplicationResult]
APPLICATION_RESULT_NOT_AVAILABLE: ApplicationResult
APPLICATION_RESULT_ACCEPTED: ApplicationResult
APPLICATION_RESULT_REJECTED: ApplicationResult
APPLICATION_RESULT_RECLAIMED: ApplicationResult

class CreatorApplication(_message.Message):
    __slots__ = ("id", "creator", "result", "decision_timestamp", "decision_maker", "decision_reason", "stake", "description", "creation_timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DECISION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DECISION_MAKER_FIELD_NUMBER: _ClassVar[int]
    DECISION_REASON_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    result: ApplicationResult
    decision_timestamp: int
    decision_maker: str
    decision_reason: str
    stake: int
    description: str
    creation_timestamp: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., result: _Optional[_Union[ApplicationResult, str]] = ..., decision_timestamp: _Optional[int] = ..., decision_maker: _Optional[str] = ..., decision_reason: _Optional[str] = ..., stake: _Optional[int] = ..., description: _Optional[str] = ..., creation_timestamp: _Optional[int] = ...) -> None: ...
