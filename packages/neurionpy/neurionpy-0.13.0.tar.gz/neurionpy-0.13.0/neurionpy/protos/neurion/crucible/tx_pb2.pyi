from amino import amino_pb2 as _amino_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from neurion.crucible import params_pb2 as _params_pb2
from neurion.crucible import task_pb2 as _task_pb2
from neurion.crucible import submission_pb2 as _submission_pb2
from neurion.crucible import score_task_pb2 as _score_task_pb2
from neurion.crucible import plagiarism_report_pb2 as _plagiarism_report_pb2
from neurion.crucible import dispute_score_task_pb2 as _dispute_score_task_pb2
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
    __slots__ = ("creator", "reward", "training_kit", "validation_kit", "duration_in_days", "name", "description")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    TRAINING_KIT_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_KIT_FIELD_NUMBER: _ClassVar[int]
    DURATION_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    creator: str
    reward: int
    training_kit: str
    validation_kit: str
    duration_in_days: int
    name: str
    description: str
    def __init__(self, creator: _Optional[str] = ..., reward: _Optional[int] = ..., training_kit: _Optional[str] = ..., validation_kit: _Optional[str] = ..., duration_in_days: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class MsgCreateTaskResponse(_message.Message):
    __slots__ = ("task",)
    TASK_FIELD_NUMBER: _ClassVar[int]
    task: _task_pb2.Task
    def __init__(self, task: _Optional[_Union[_task_pb2.Task, _Mapping]] = ...) -> None: ...

class MsgRegisterTrainer(_message.Message):
    __slots__ = ("creator", "stake", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    stake: int
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., stake: _Optional[int] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgRegisterTrainerResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgRegisterScorer(_message.Message):
    __slots__ = ("creator", "stake", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    stake: int
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., stake: _Optional[int] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgRegisterScorerResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgSubmitTrainingResult(_message.Message):
    __slots__ = ("creator", "task_id", "result", "metainfo", "encrypted_proof_of_ownership")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    METAINFO_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_PROOF_OF_OWNERSHIP_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    result: str
    metainfo: str
    encrypted_proof_of_ownership: str
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ..., result: _Optional[str] = ..., metainfo: _Optional[str] = ..., encrypted_proof_of_ownership: _Optional[str] = ...) -> None: ...

class MsgSubmitTrainingResultResponse(_message.Message):
    __slots__ = ("submission",)
    SUBMISSION_FIELD_NUMBER: _ClassVar[int]
    submission: _submission_pb2.Submission
    def __init__(self, submission: _Optional[_Union[_submission_pb2.Submission, _Mapping]] = ...) -> None: ...

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

class MsgRequestScoringTask(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgRequestScoringTaskResponse(_message.Message):
    __slots__ = ("score_task",)
    SCORE_TASK_FIELD_NUMBER: _ClassVar[int]
    score_task: _score_task_pb2.ScoreTask
    def __init__(self, score_task: _Optional[_Union[_score_task_pb2.ScoreTask, _Mapping]] = ...) -> None: ...

class MsgSubmitScore(_message.Message):
    __slots__ = ("creator", "score_task_id", "score")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    creator: str
    score_task_id: int
    score: str
    def __init__(self, creator: _Optional[str] = ..., score_task_id: _Optional[int] = ..., score: _Optional[str] = ...) -> None: ...

class MsgSubmitScoreResponse(_message.Message):
    __slots__ = ("score_task",)
    SCORE_TASK_FIELD_NUMBER: _ClassVar[int]
    score_task: _score_task_pb2.ScoreTask
    def __init__(self, score_task: _Optional[_Union[_score_task_pb2.ScoreTask, _Mapping]] = ...) -> None: ...

class MsgSubmitFinalResult(_message.Message):
    __slots__ = ("creator", "task_id", "result", "metainfo", "encrypted_proof_of_ownership")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    METAINFO_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_PROOF_OF_OWNERSHIP_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    result: str
    metainfo: str
    encrypted_proof_of_ownership: str
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ..., result: _Optional[str] = ..., metainfo: _Optional[str] = ..., encrypted_proof_of_ownership: _Optional[str] = ...) -> None: ...

class MsgSubmitFinalResultResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgReportModelPlagiarism(_message.Message):
    __slots__ = ("creator", "my_submission_id", "suspected_submission_id", "encrypt_key")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    MY_SUBMISSION_ID_FIELD_NUMBER: _ClassVar[int]
    SUSPECTED_SUBMISSION_ID_FIELD_NUMBER: _ClassVar[int]
    ENCRYPT_KEY_FIELD_NUMBER: _ClassVar[int]
    creator: str
    my_submission_id: int
    suspected_submission_id: int
    encrypt_key: str
    def __init__(self, creator: _Optional[str] = ..., my_submission_id: _Optional[int] = ..., suspected_submission_id: _Optional[int] = ..., encrypt_key: _Optional[str] = ...) -> None: ...

class MsgReportModelPlagiarismResponse(_message.Message):
    __slots__ = ("report",)
    REPORT_FIELD_NUMBER: _ClassVar[int]
    report: _plagiarism_report_pb2.PlagiarismReport
    def __init__(self, report: _Optional[_Union[_plagiarism_report_pb2.PlagiarismReport, _Mapping]] = ...) -> None: ...

class MsgAcceptPlagiarismReport(_message.Message):
    __slots__ = ("creator", "report_id", "proof_of_plagiarism")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    PROOF_OF_PLAGIARISM_FIELD_NUMBER: _ClassVar[int]
    creator: str
    report_id: int
    proof_of_plagiarism: str
    def __init__(self, creator: _Optional[str] = ..., report_id: _Optional[int] = ..., proof_of_plagiarism: _Optional[str] = ...) -> None: ...

class MsgAcceptPlagiarismReportResponse(_message.Message):
    __slots__ = ("report",)
    REPORT_FIELD_NUMBER: _ClassVar[int]
    report: _plagiarism_report_pb2.PlagiarismReport
    def __init__(self, report: _Optional[_Union[_plagiarism_report_pb2.PlagiarismReport, _Mapping]] = ...) -> None: ...

class MsgRejectPlagiarismReport(_message.Message):
    __slots__ = ("creator", "report_id", "reason")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    creator: str
    report_id: int
    reason: str
    def __init__(self, creator: _Optional[str] = ..., report_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class MsgRejectPlagiarismReportResponse(_message.Message):
    __slots__ = ("report",)
    REPORT_FIELD_NUMBER: _ClassVar[int]
    report: _plagiarism_report_pb2.PlagiarismReport
    def __init__(self, report: _Optional[_Union[_plagiarism_report_pb2.PlagiarismReport, _Mapping]] = ...) -> None: ...

class MsgDisputeSubmissionScore(_message.Message):
    __slots__ = ("creator", "submission_id", "score")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    creator: str
    submission_id: int
    score: str
    def __init__(self, creator: _Optional[str] = ..., submission_id: _Optional[int] = ..., score: _Optional[str] = ...) -> None: ...

class MsgDisputeSubmissionScoreResponse(_message.Message):
    __slots__ = ("dispute_score_task",)
    DISPUTE_SCORE_TASK_FIELD_NUMBER: _ClassVar[int]
    dispute_score_task: _dispute_score_task_pb2.DisputeScoreTask
    def __init__(self, dispute_score_task: _Optional[_Union[_dispute_score_task_pb2.DisputeScoreTask, _Mapping]] = ...) -> None: ...

class MsgStartTask(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgStartTaskResponse(_message.Message):
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

class MsgTriggerTaskToFinalSubmission(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class MsgTriggerTaskToFinalSubmissionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MsgTriggerTaskToFinalTesting(_message.Message):
    __slots__ = ("creator", "task_id", "test_kit")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_KIT_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    test_kit: str
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ..., test_kit: _Optional[str] = ...) -> None: ...

class MsgTriggerTaskToFinalTestingResponse(_message.Message):
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
