from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_STATUS_CREATED: _ClassVar[TaskStatus]
    TASK_STATUS_PROPOSING: _ClassVar[TaskStatus]
    TASK_STATUS_TESTING: _ClassVar[TaskStatus]
    TASK_STATUS_DISPUTE: _ClassVar[TaskStatus]
    TASK_STATUS_TERMINATED: _ClassVar[TaskStatus]
    TASK_STATUS_ABORTED: _ClassVar[TaskStatus]
TASK_STATUS_CREATED: TaskStatus
TASK_STATUS_PROPOSING: TaskStatus
TASK_STATUS_TESTING: TaskStatus
TASK_STATUS_DISPUTE: TaskStatus
TASK_STATUS_TERMINATED: TaskStatus
TASK_STATUS_ABORTED: TaskStatus

class Task(_message.Message):
    __slots__ = ("id", "creator", "name", "description", "reward", "base_models", "test_data", "created_timestamp", "proposed_timestamps", "testing_timestamps", "dispute_timestamps", "terminated_timestamp", "aborted_timestamp", "status", "max_rounds", "current_round")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    BASE_MODELS_FIELD_NUMBER: _ClassVar[int]
    TEST_DATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    TESTING_TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    DISPUTE_TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    TERMINATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ABORTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MAX_ROUNDS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ROUND_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    name: str
    description: str
    reward: int
    base_models: _containers.RepeatedScalarFieldContainer[str]
    test_data: _containers.RepeatedScalarFieldContainer[str]
    created_timestamp: int
    proposed_timestamps: _containers.RepeatedScalarFieldContainer[int]
    testing_timestamps: _containers.RepeatedScalarFieldContainer[int]
    dispute_timestamps: _containers.RepeatedScalarFieldContainer[int]
    terminated_timestamp: int
    aborted_timestamp: int
    status: TaskStatus
    max_rounds: int
    current_round: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., reward: _Optional[int] = ..., base_models: _Optional[_Iterable[str]] = ..., test_data: _Optional[_Iterable[str]] = ..., created_timestamp: _Optional[int] = ..., proposed_timestamps: _Optional[_Iterable[int]] = ..., testing_timestamps: _Optional[_Iterable[int]] = ..., dispute_timestamps: _Optional[_Iterable[int]] = ..., terminated_timestamp: _Optional[int] = ..., aborted_timestamp: _Optional[int] = ..., status: _Optional[_Union[TaskStatus, str]] = ..., max_rounds: _Optional[int] = ..., current_round: _Optional[int] = ...) -> None: ...
