from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from neurion.fusion import params_pb2 as _params_pb2
from neurion.fusion import task_pb2 as _task_pb2
from neurion.fusion import creator_application_pb2 as _creator_application_pb2
from neurion.fusion import proposed_model_pb2 as _proposed_model_pb2
from neurion.fusion import validation_task_pb2 as _validation_task_pb2
from neurion.fusion import dispute_validation_task_pb2 as _dispute_validation_task_pb2
from neurion.fusion import error_code_pb2 as _error_code_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryParamsResponse(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ...) -> None: ...

class QueryGetTaskRequest(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class QueryGetTaskResponse(_message.Message):
    __slots__ = ("task",)
    TASK_FIELD_NUMBER: _ClassVar[int]
    task: _task_pb2.Task
    def __init__(self, task: _Optional[_Union[_task_pb2.Task, _Mapping]] = ...) -> None: ...

class QueryGetTaskRewardRequest(_message.Message):
    __slots__ = ("task_id", "user")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    user: str
    def __init__(self, task_id: _Optional[int] = ..., user: _Optional[str] = ...) -> None: ...

class QueryGetTaskRewardResponse(_message.Message):
    __slots__ = ("reward",)
    REWARD_FIELD_NUMBER: _ClassVar[int]
    reward: int
    def __init__(self, reward: _Optional[int] = ...) -> None: ...

class QueryGetCreatorApplicationsRequest(_message.Message):
    __slots__ = ("creator",)
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    def __init__(self, creator: _Optional[str] = ...) -> None: ...

class QueryGetCreatorApplicationsResponse(_message.Message):
    __slots__ = ("applicants",)
    APPLICANTS_FIELD_NUMBER: _ClassVar[int]
    applicants: _containers.RepeatedCompositeFieldContainer[_creator_application_pb2.CreatorApplication]
    def __init__(self, applicants: _Optional[_Iterable[_Union[_creator_application_pb2.CreatorApplication, _Mapping]]] = ...) -> None: ...

class QueryGetPendingCreatorApplicationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetPendingCreatorApplicationsResponse(_message.Message):
    __slots__ = ("applicants",)
    APPLICANTS_FIELD_NUMBER: _ClassVar[int]
    applicants: _containers.RepeatedCompositeFieldContainer[_creator_application_pb2.CreatorApplication]
    def __init__(self, applicants: _Optional[_Iterable[_Union[_creator_application_pb2.CreatorApplication, _Mapping]]] = ...) -> None: ...

class QueryGetModelsByRoundRequest(_message.Message):
    __slots__ = ("task_id", "round")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    round: int
    def __init__(self, task_id: _Optional[int] = ..., round: _Optional[int] = ...) -> None: ...

class QueryGetModelsByRoundResponse(_message.Message):
    __slots__ = ("models",)
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[_proposed_model_pb2.ProposedModel]
    def __init__(self, models: _Optional[_Iterable[_Union[_proposed_model_pb2.ProposedModel, _Mapping]]] = ...) -> None: ...

class QueryGetTaskStakeRequest(_message.Message):
    __slots__ = ("task_id", "user")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    user: str
    def __init__(self, task_id: _Optional[int] = ..., user: _Optional[str] = ...) -> None: ...

class QueryGetTaskStakeResponse(_message.Message):
    __slots__ = ("stake",)
    STAKE_FIELD_NUMBER: _ClassVar[int]
    stake: int
    def __init__(self, stake: _Optional[int] = ...) -> None: ...

class QueryGetValidationTaskRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryGetValidationTaskResponse(_message.Message):
    __slots__ = ("validation_task",)
    VALIDATION_TASK_FIELD_NUMBER: _ClassVar[int]
    validation_task: _validation_task_pb2.ValidationTask
    def __init__(self, validation_task: _Optional[_Union[_validation_task_pb2.ValidationTask, _Mapping]] = ...) -> None: ...

class QueryCanTriggerTestingForRoundRequest(_message.Message):
    __slots__ = ("user", "task_id", "round")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    round: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ..., round: _Optional[int] = ...) -> None: ...

class QueryCanTriggerTestingForRoundResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanStartNewRoundRequest(_message.Message):
    __slots__ = ("user", "task_id", "round")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    round: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ..., round: _Optional[int] = ...) -> None: ...

class QueryCanStartNewRoundResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanRegisterAsProposerRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanRegisterAsProposerResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanRegisterAsValidatorRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanRegisterAsValidatorResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryIsProposerRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryIsProposerResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryIsValidatorRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryIsValidatorResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanProposeModelRequest(_message.Message):
    __slots__ = ("user", "task_id", "round")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    round: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ..., round: _Optional[int] = ...) -> None: ...

class QueryCanProposeModelResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanRequestValidationTaskRequest(_message.Message):
    __slots__ = ("user", "task_id", "round")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    round: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ..., round: _Optional[int] = ...) -> None: ...

class QueryCanRequestValidationTaskResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryGetPendingValidationTasksRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryGetPendingValidationTasksResponse(_message.Message):
    __slots__ = ("validation_tasks",)
    VALIDATION_TASKS_FIELD_NUMBER: _ClassVar[int]
    validation_tasks: _containers.RepeatedCompositeFieldContainer[_validation_task_pb2.ValidationTask]
    def __init__(self, validation_tasks: _Optional[_Iterable[_Union[_validation_task_pb2.ValidationTask, _Mapping]]] = ...) -> None: ...

class QueryCanTerminateRequest(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanTerminateResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryGetScoreDisputeFromUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...

class QueryGetScoreDisputeFromUserResponse(_message.Message):
    __slots__ = ("dispute_validation_tasks",)
    DISPUTE_VALIDATION_TASKS_FIELD_NUMBER: _ClassVar[int]
    dispute_validation_tasks: _containers.RepeatedCompositeFieldContainer[_dispute_validation_task_pb2.DisputeValidationTask]
    def __init__(self, dispute_validation_tasks: _Optional[_Iterable[_Union[_dispute_validation_task_pb2.DisputeValidationTask, _Mapping]]] = ...) -> None: ...
