from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DisputeValidationTaskResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISPUTE_VALIDATION_TASK_RESULT_NOT_AVAILABLE: _ClassVar[DisputeValidationTaskResult]
    DISPUTE_VALIDATION_TASK_RESULT_ACCEPTED: _ClassVar[DisputeValidationTaskResult]
    DISPUTE_VALIDATION_TASK_RESULT_REJECTED: _ClassVar[DisputeValidationTaskResult]
DISPUTE_VALIDATION_TASK_RESULT_NOT_AVAILABLE: DisputeValidationTaskResult
DISPUTE_VALIDATION_TASK_RESULT_ACCEPTED: DisputeValidationTaskResult
DISPUTE_VALIDATION_TASK_RESULT_REJECTED: DisputeValidationTaskResult

class DisputeValidationTask(_message.Message):
    __slots__ = ("id", "creator", "proposed_model_id", "proposed_score", "deposit", "result", "created_timestamp", "decision_timestamp", "accepting_dispute_validators", "rejecting_dispute_validators", "task_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_SCORE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DECISION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ACCEPTING_DISPUTE_VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    REJECTING_DISPUTE_VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    proposed_model_id: int
    proposed_score: str
    deposit: int
    result: DisputeValidationTaskResult
    created_timestamp: int
    decision_timestamp: int
    accepting_dispute_validators: _containers.RepeatedScalarFieldContainer[str]
    rejecting_dispute_validators: _containers.RepeatedScalarFieldContainer[str]
    task_id: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., proposed_model_id: _Optional[int] = ..., proposed_score: _Optional[str] = ..., deposit: _Optional[int] = ..., result: _Optional[_Union[DisputeValidationTaskResult, str]] = ..., created_timestamp: _Optional[int] = ..., decision_timestamp: _Optional[int] = ..., accepting_dispute_validators: _Optional[_Iterable[str]] = ..., rejecting_dispute_validators: _Optional[_Iterable[str]] = ..., task_id: _Optional[int] = ...) -> None: ...
