from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DisputeScoreTaskResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISPUTE_SCORE_TASK_RESULT_NOT_AVAILABLE: _ClassVar[DisputeScoreTaskResult]
    DISPUTE_SCORE_TASK_RESULT_ACCEPTED: _ClassVar[DisputeScoreTaskResult]
    DISPUTE_SCORE_TASK_RESULT_REJECTED: _ClassVar[DisputeScoreTaskResult]
DISPUTE_SCORE_TASK_RESULT_NOT_AVAILABLE: DisputeScoreTaskResult
DISPUTE_SCORE_TASK_RESULT_ACCEPTED: DisputeScoreTaskResult
DISPUTE_SCORE_TASK_RESULT_REJECTED: DisputeScoreTaskResult

class DisputeScoreTask(_message.Message):
    __slots__ = ("id", "creator", "submission_id", "proposed_score", "deposit", "result", "created_timestamp", "decision_timestamp", "accepting_dispute_scorers", "rejecting_dispute_scorers", "task_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_ID_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_SCORE_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DECISION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ACCEPTING_DISPUTE_SCORERS_FIELD_NUMBER: _ClassVar[int]
    REJECTING_DISPUTE_SCORERS_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    submission_id: int
    proposed_score: str
    deposit: int
    result: DisputeScoreTaskResult
    created_timestamp: int
    decision_timestamp: int
    accepting_dispute_scorers: _containers.RepeatedScalarFieldContainer[str]
    rejecting_dispute_scorers: _containers.RepeatedScalarFieldContainer[str]
    task_id: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., submission_id: _Optional[int] = ..., proposed_score: _Optional[str] = ..., deposit: _Optional[int] = ..., result: _Optional[_Union[DisputeScoreTaskResult, str]] = ..., created_timestamp: _Optional[int] = ..., decision_timestamp: _Optional[int] = ..., accepting_dispute_scorers: _Optional[_Iterable[str]] = ..., rejecting_dispute_scorers: _Optional[_Iterable[str]] = ..., task_id: _Optional[int] = ...) -> None: ...
