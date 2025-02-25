from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_STATUS_CREATED: _ClassVar[TaskStatus]
    TASK_STATUS_STARTED: _ClassVar[TaskStatus]
    TASK_STATUS_ABORTED: _ClassVar[TaskStatus]
    TASK_STATUS_FINAL_SUBMISSION: _ClassVar[TaskStatus]
    TASK_STATUS_FINAL_TESTING: _ClassVar[TaskStatus]
    TASK_STATUS_FINAL_DISPUTE: _ClassVar[TaskStatus]
    TASK_STATUS_TERMINATED: _ClassVar[TaskStatus]
TASK_STATUS_CREATED: TaskStatus
TASK_STATUS_STARTED: TaskStatus
TASK_STATUS_ABORTED: TaskStatus
TASK_STATUS_FINAL_SUBMISSION: TaskStatus
TASK_STATUS_FINAL_TESTING: TaskStatus
TASK_STATUS_FINAL_DISPUTE: TaskStatus
TASK_STATUS_TERMINATED: TaskStatus

class Task(_message.Message):
    __slots__ = ("id", "creator", "name", "description", "reward", "duration_in_days", "training_kit", "validation_kit", "final_test_kit", "status", "created_timestamp", "started_timestamp", "terminated_timestamp", "final_submission_timestamp", "final_testing_timestamp", "final_dispute_timestamp", "aborted_timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    DURATION_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    TRAINING_KIT_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_KIT_FIELD_NUMBER: _ClassVar[int]
    FINAL_TEST_KIT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STARTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TERMINATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FINAL_SUBMISSION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FINAL_TESTING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FINAL_DISPUTE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ABORTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    name: str
    description: str
    reward: int
    duration_in_days: int
    training_kit: str
    validation_kit: str
    final_test_kit: str
    status: TaskStatus
    created_timestamp: int
    started_timestamp: int
    terminated_timestamp: int
    final_submission_timestamp: int
    final_testing_timestamp: int
    final_dispute_timestamp: int
    aborted_timestamp: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., reward: _Optional[int] = ..., duration_in_days: _Optional[int] = ..., training_kit: _Optional[str] = ..., validation_kit: _Optional[str] = ..., final_test_kit: _Optional[str] = ..., status: _Optional[_Union[TaskStatus, str]] = ..., created_timestamp: _Optional[int] = ..., started_timestamp: _Optional[int] = ..., terminated_timestamp: _Optional[int] = ..., final_submission_timestamp: _Optional[int] = ..., final_testing_timestamp: _Optional[int] = ..., final_dispute_timestamp: _Optional[int] = ..., aborted_timestamp: _Optional[int] = ...) -> None: ...
