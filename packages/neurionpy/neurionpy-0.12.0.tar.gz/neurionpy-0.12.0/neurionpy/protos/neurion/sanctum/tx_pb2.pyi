from amino import amino_pb2 as _amino_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from neurion.sanctum import params_pb2 as _params_pb2
from neurion.sanctum import dataset_application_pb2 as _dataset_application_pb2
from neurion.sanctum import dataset_usage_request_pb2 as _dataset_usage_request_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgUpdateParams(_message.Message):
    __slots__ = ("authority", "params")
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    authority: str
    params: _params_pb2.Params
    def __init__(self, authority: _Optional[str] = ..., params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...

class MsgUpdateParamsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgSubmitDatasetApplication(_message.Message):
    __slots__ = ("creator", "encrypted_data_link", "explanation_link", "contact", "stake", "proof_of_authenticity", "dataset_usage_fee")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_DATA_LINK_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_LINK_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    PROOF_OF_AUTHENTICITY_FIELD_NUMBER: _ClassVar[int]
    DATASET_USAGE_FEE_FIELD_NUMBER: _ClassVar[int]
    creator: str
    encrypted_data_link: str
    explanation_link: str
    contact: str
    stake: int
    proof_of_authenticity: str
    dataset_usage_fee: int
    def __init__(self, creator: _Optional[str] = ..., encrypted_data_link: _Optional[str] = ..., explanation_link: _Optional[str] = ..., contact: _Optional[str] = ..., stake: _Optional[int] = ..., proof_of_authenticity: _Optional[str] = ..., dataset_usage_fee: _Optional[int] = ...) -> None: ...

class MsgSubmitDatasetApplicationResponse(_message.Message):
    __slots__ = ("dataset_application",)
    DATASET_APPLICATION_FIELD_NUMBER: _ClassVar[int]
    dataset_application: _dataset_application_pb2.DatasetApplication
    def __init__(self, dataset_application: _Optional[_Union[_dataset_application_pb2.DatasetApplication, _Mapping]] = ...) -> None: ...

class MsgApproveApplication(_message.Message):
    __slots__ = ("creator", "application_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    application_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., application_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgApproveApplicationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRejectApplication(_message.Message):
    __slots__ = ("creator", "application_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    application_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., application_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgRejectApplicationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgDisclaimDataset(_message.Message):
    __slots__ = ("creator", "application_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    application_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., application_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgDisclaimDatasetResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRequestToUseDataset(_message.Message):
    __slots__ = ("creator", "dataset_id", "intent", "training_repository", "contact")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    TRAINING_REPOSITORY_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    dataset_id: int
    intent: str
    training_repository: str
    contact: str
    def __init__(self, creator: _Optional[str] = ..., dataset_id: _Optional[int] = ..., intent: _Optional[str] = ..., training_repository: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class MsgRequestToUseDatasetResponse(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _dataset_usage_request_pb2.DatasetUsageRequest
    def __init__(self, request: _Optional[_Union[_dataset_usage_request_pb2.DatasetUsageRequest, _Mapping]] = ...) -> None: ...

class MsgCancelDatasetUsageRequest(_message.Message):
    __slots__ = ("creator", "request_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgCancelDatasetUsageRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRejectDatasetUsageRequest(_message.Message):
    __slots__ = ("creator", "request_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgRejectDatasetUsageRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgApproveDatasetUsageRequest(_message.Message):
    __slots__ = ("creator", "request_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgApproveDatasetUsageRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgAddProcessor(_message.Message):
    __slots__ = ("creator", "processor")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    processor: str
    def __init__(self, creator: _Optional[str] = ..., processor: _Optional[str] = ...) -> None: ...

class MsgAddProcessorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRemoveProcessor(_message.Message):
    __slots__ = ("creator", "processor")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    processor: str
    def __init__(self, creator: _Optional[str] = ..., processor: _Optional[str] = ...) -> None: ...

class MsgRemoveProcessorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgProcessDatasetUsageRequest(_message.Message):
    __slots__ = ("creator", "request_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ...) -> None: ...

class MsgProcessDatasetUsageRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgFinishDatasetUsageRequest(_message.Message):
    __slots__ = ("creator", "request_id", "feedback")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    feedback: str
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ..., feedback: _Optional[str] = ...) -> None: ...

class MsgFinishDatasetUsageRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgDisputeDatasetUsageRequest(_message.Message):
    __slots__ = ("creator", "request_id", "model", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    model: str
    reason: str
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ..., model: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgDisputeDatasetUsageRequestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgApproveDispute(_message.Message):
    __slots__ = ("creator", "request_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgApproveDisputeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRejectDispute(_message.Message):
    __slots__ = ("creator", "request_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    request_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., request_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgRejectDisputeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgStakeToSanctum(_message.Message):
    __slots__ = ("creator", "amount")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    amount: int
    def __init__(self, creator: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class MsgStakeToSanctumResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUnstakeFromSanctum(_message.Message):
    __slots__ = ("creator", "amount")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    amount: int
    def __init__(self, creator: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class MsgUnstakeFromSanctumResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgClaimReward(_message.Message):
    __slots__ = ("creator",)
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    def __init__(self, creator: _Optional[str] = ...) -> None: ...

class MsgClaimRewardResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
