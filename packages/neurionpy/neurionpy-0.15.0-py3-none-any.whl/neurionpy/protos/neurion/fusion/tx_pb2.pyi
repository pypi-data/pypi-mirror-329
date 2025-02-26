from amino import amino_pb2 as _amino_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from neurion.fusion import params_pb2 as _params_pb2
from neurion.fusion import task_pb2 as _task_pb2
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

class MsgApplyCreator(_message.Message):
    __slots__ = ("creator", "description")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    creator: str
    description: str
    def __init__(self, creator: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class MsgApplyCreatorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

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

class MsgCreateTask(_message.Message):
    __slots__ = ("creator", "base_model", "max_rounds", "reward", "name", "description")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    MAX_ROUNDS_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    creator: str
    base_model: str
    max_rounds: int
    reward: int
    name: str
    description: str
    def __init__(self, creator: _Optional[str] = ..., base_model: _Optional[str] = ..., max_rounds: _Optional[int] = ..., reward: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class MsgCreateTaskResponse(_message.Message):
    __slots__ = ("task",)
    TASK_FIELD_NUMBER: _ClassVar[int]
    task: _task_pb2.Task
    def __init__(self, task: _Optional[_Union[_task_pb2.Task, _Mapping]] = ...) -> None: ...

class MsgStartTask(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgStartTaskResponse(_message.Message):
    __slots__ = ("task",)
    TASK_FIELD_NUMBER: _ClassVar[int]
    task: _task_pb2.Task
    def __init__(self, task: _Optional[_Union[_task_pb2.Task, _Mapping]] = ...) -> None: ...

class MsgProposeModel(_message.Message):
    __slots__ = ("creator", "task_id", "model", "metainfo", "round")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    METAINFO_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    model: str
    metainfo: str
    round: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ..., model: _Optional[str] = ..., metainfo: _Optional[str] = ..., round: _Optional[int] = ...) -> None: ...

class MsgProposeModelResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRegisterProposer(_message.Message):
    __slots__ = ("creator", "stake", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    stake: int
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., stake: _Optional[int] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgRegisterProposerResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRegisterValidator(_message.Message):
    __slots__ = ("creator", "stake", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    stake: int
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., stake: _Optional[int] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgRegisterValidatorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgStartTesting(_message.Message):
    __slots__ = ("creator", "round", "testset", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    TESTSET_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    round: int
    testset: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., round: _Optional[int] = ..., testset: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgStartTestingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRequestValidationTask(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgRequestValidationTaskResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgSubmitScore(_message.Message):
    __slots__ = ("creator", "validation_task_id", "score")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    creator: str
    validation_task_id: int
    score: str
    def __init__(self, creator: _Optional[str] = ..., validation_task_id: _Optional[int] = ..., score: _Optional[str] = ...) -> None: ...

class MsgSubmitScoreResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgDisputeModelScore(_message.Message):
    __slots__ = ("creator", "model_id", "score")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    creator: str
    model_id: int
    score: str
    def __init__(self, creator: _Optional[str] = ..., model_id: _Optional[int] = ..., score: _Optional[str] = ...) -> None: ...

class MsgDisputeModelScoreResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgStartNewRound(_message.Message):
    __slots__ = ("creator", "round", "base_model", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    round: int
    base_model: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., round: _Optional[int] = ..., base_model: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgStartNewRoundResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgTerminateTask(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgTerminateTaskResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgStakeToTask(_message.Message):
    __slots__ = ("creator", "task_id", "amount")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    amount: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ..., amount: _Optional[int] = ...) -> None: ...

class MsgStakeToTaskResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgClaimTaskReward(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgClaimTaskRewardResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgUnstakeFromTask(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgUnstakeFromTaskResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgDisclaimCreatorStatus(_message.Message):
    __slots__ = ("creator", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    reason: str
    def __init__(self, creator: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgDisclaimCreatorStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgAbortTask(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgAbortTaskResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
