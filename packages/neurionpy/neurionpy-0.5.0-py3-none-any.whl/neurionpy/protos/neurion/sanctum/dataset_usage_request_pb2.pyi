from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DatasetUsageRequestResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_USAGE_REQUEST_RESULT_NOT_AVAILABLE: _ClassVar[DatasetUsageRequestResult]
    DATASET_USAGE_REQUEST_RESULT_ACCEPTED: _ClassVar[DatasetUsageRequestResult]
    DATASET_USAGE_REQUEST_RESULT_REJECTED: _ClassVar[DatasetUsageRequestResult]
    DATASET_USAGE_REQUEST_RESULT_CANCELLED: _ClassVar[DatasetUsageRequestResult]
    DATASET_USAGE_REQUEST_RESULT_PROCESSING: _ClassVar[DatasetUsageRequestResult]
    DATASET_USAGE_REQUEST_RESULT_FINISHED: _ClassVar[DatasetUsageRequestResult]
    DATASET_USAGE_REQUEST_RESULT_DISPUTED: _ClassVar[DatasetUsageRequestResult]
DATASET_USAGE_REQUEST_RESULT_NOT_AVAILABLE: DatasetUsageRequestResult
DATASET_USAGE_REQUEST_RESULT_ACCEPTED: DatasetUsageRequestResult
DATASET_USAGE_REQUEST_RESULT_REJECTED: DatasetUsageRequestResult
DATASET_USAGE_REQUEST_RESULT_CANCELLED: DatasetUsageRequestResult
DATASET_USAGE_REQUEST_RESULT_PROCESSING: DatasetUsageRequestResult
DATASET_USAGE_REQUEST_RESULT_FINISHED: DatasetUsageRequestResult
DATASET_USAGE_REQUEST_RESULT_DISPUTED: DatasetUsageRequestResult

class DatasetUsageRequest(_message.Message):
    __slots__ = ("id", "creator", "result", "dataset_id", "intent", "training_repository", "fee_paid", "decision_timestamp", "decision_maker", "decision_reason", "creation_timestamp", "dispute_model", "dispute_resolution_reason", "feedback", "contact")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    TRAINING_REPOSITORY_FIELD_NUMBER: _ClassVar[int]
    FEE_PAID_FIELD_NUMBER: _ClassVar[int]
    DECISION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DECISION_MAKER_FIELD_NUMBER: _ClassVar[int]
    DECISION_REASON_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DISPUTE_MODEL_FIELD_NUMBER: _ClassVar[int]
    DISPUTE_RESOLUTION_REASON_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    result: DatasetUsageRequestResult
    dataset_id: int
    intent: str
    training_repository: str
    fee_paid: int
    decision_timestamp: int
    decision_maker: str
    decision_reason: str
    creation_timestamp: int
    dispute_model: str
    dispute_resolution_reason: str
    feedback: str
    contact: str
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., result: _Optional[_Union[DatasetUsageRequestResult, str]] = ..., dataset_id: _Optional[int] = ..., intent: _Optional[str] = ..., training_repository: _Optional[str] = ..., fee_paid: _Optional[int] = ..., decision_timestamp: _Optional[int] = ..., decision_maker: _Optional[str] = ..., decision_reason: _Optional[str] = ..., creation_timestamp: _Optional[int] = ..., dispute_model: _Optional[str] = ..., dispute_resolution_reason: _Optional[str] = ..., feedback: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...
