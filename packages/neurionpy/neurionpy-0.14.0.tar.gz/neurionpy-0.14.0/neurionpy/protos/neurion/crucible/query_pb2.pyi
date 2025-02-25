from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from neurion.crucible import params_pb2 as _params_pb2
from neurion.crucible import task_pb2 as _task_pb2
from neurion.crucible import submission_pb2 as _submission_pb2
from neurion.crucible import plagiarism_report_pb2 as _plagiarism_report_pb2
from neurion.crucible import creator_application_pb2 as _creator_application_pb2
from neurion.crucible import score_task_pb2 as _score_task_pb2
from neurion.crucible import error_code_pb2 as _error_code_pb2
from neurion.crucible import dispute_score_task_pb2 as _dispute_score_task_pb2
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

class QueryGetCreatorsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetCreatorsResponse(_message.Message):
    __slots__ = ("creators",)
    CREATORS_FIELD_NUMBER: _ClassVar[int]
    creators: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, creators: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryGetCreatorApplicationsRequest(_message.Message):
    __slots__ = ("creator",)
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    creator: str
    def __init__(self, creator: _Optional[str] = ...) -> None: ...

class QueryGetCreatorApplicationsResponse(_message.Message):
    __slots__ = ("applications",)
    APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    applications: _containers.RepeatedCompositeFieldContainer[_creator_application_pb2.CreatorApplication]
    def __init__(self, applications: _Optional[_Iterable[_Union[_creator_application_pb2.CreatorApplication, _Mapping]]] = ...) -> None: ...

class QueryGetTaskRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryGetTaskResponse(_message.Message):
    __slots__ = ("task",)
    TASK_FIELD_NUMBER: _ClassVar[int]
    task: _task_pb2.Task
    def __init__(self, task: _Optional[_Union[_task_pb2.Task, _Mapping]] = ...) -> None: ...

class QueryListAllTasksRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(self, offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryListAllTasksResponse(_message.Message):
    __slots__ = ("tasks", "pagination")
    TASKS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[_task_pb2.Task]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, tasks: _Optional[_Iterable[_Union[_task_pb2.Task, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryListTasksByStatusRequest(_message.Message):
    __slots__ = ("status", "offset", "limit")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    status: _task_pb2.TaskStatus
    offset: int
    limit: int
    def __init__(self, status: _Optional[_Union[_task_pb2.TaskStatus, str]] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class QueryListTasksByStatusResponse(_message.Message):
    __slots__ = ("tasks", "pagination")
    TASKS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[_task_pb2.Task]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, tasks: _Optional[_Iterable[_Union[_task_pb2.Task, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryGetSubmissionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryGetSubmissionResponse(_message.Message):
    __slots__ = ("submission",)
    SUBMISSION_FIELD_NUMBER: _ClassVar[int]
    submission: _submission_pb2.Submission
    def __init__(self, submission: _Optional[_Union[_submission_pb2.Submission, _Mapping]] = ...) -> None: ...

class QueryGetSubmissionByTaskCreatorRequest(_message.Message):
    __slots__ = ("task_id", "creator")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    creator: str
    def __init__(self, task_id: _Optional[int] = ..., creator: _Optional[str] = ...) -> None: ...

class QueryGetSubmissionByTaskCreatorResponse(_message.Message):
    __slots__ = ("final_submissions", "provisional_submissions")
    FINAL_SUBMISSIONS_FIELD_NUMBER: _ClassVar[int]
    PROVISIONAL_SUBMISSIONS_FIELD_NUMBER: _ClassVar[int]
    final_submissions: _containers.RepeatedCompositeFieldContainer[_submission_pb2.Submission]
    provisional_submissions: _containers.RepeatedCompositeFieldContainer[_submission_pb2.Submission]
    def __init__(self, final_submissions: _Optional[_Iterable[_Union[_submission_pb2.Submission, _Mapping]]] = ..., provisional_submissions: _Optional[_Iterable[_Union[_submission_pb2.Submission, _Mapping]]] = ...) -> None: ...

class QueryGetSubmissionByTaskRequest(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class QueryGetSubmissionByTaskResponse(_message.Message):
    __slots__ = ("final_submissions", "provisional_submissions")
    FINAL_SUBMISSIONS_FIELD_NUMBER: _ClassVar[int]
    PROVISIONAL_SUBMISSIONS_FIELD_NUMBER: _ClassVar[int]
    final_submissions: _containers.RepeatedCompositeFieldContainer[_submission_pb2.Submission]
    provisional_submissions: _containers.RepeatedCompositeFieldContainer[_submission_pb2.Submission]
    def __init__(self, final_submissions: _Optional[_Iterable[_Union[_submission_pb2.Submission, _Mapping]]] = ..., provisional_submissions: _Optional[_Iterable[_Union[_submission_pb2.Submission, _Mapping]]] = ...) -> None: ...

class QueryGetEncryptedProofOfOwnershipRequest(_message.Message):
    __slots__ = ("key", "plaintext")
    KEY_FIELD_NUMBER: _ClassVar[int]
    PLAINTEXT_FIELD_NUMBER: _ClassVar[int]
    key: str
    plaintext: str
    def __init__(self, key: _Optional[str] = ..., plaintext: _Optional[str] = ...) -> None: ...

class QueryGetEncryptedProofOfOwnershipResponse(_message.Message):
    __slots__ = ("ciphertext",)
    CIPHERTEXT_FIELD_NUMBER: _ClassVar[int]
    ciphertext: str
    def __init__(self, ciphertext: _Optional[str] = ...) -> None: ...

class QueryGetPlagiarismReportRequest(_message.Message):
    __slots__ = ("report_id",)
    REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    report_id: int
    def __init__(self, report_id: _Optional[int] = ...) -> None: ...

class QueryGetPlagiarismReportResponse(_message.Message):
    __slots__ = ("report",)
    REPORT_FIELD_NUMBER: _ClassVar[int]
    report: _plagiarism_report_pb2.PlagiarismReport
    def __init__(self, report: _Optional[_Union[_plagiarism_report_pb2.PlagiarismReport, _Mapping]] = ...) -> None: ...

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

class QueryGetPendingCreatorApplicationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryGetPendingCreatorApplicationsResponse(_message.Message):
    __slots__ = ("applicants",)
    APPLICANTS_FIELD_NUMBER: _ClassVar[int]
    applicants: _containers.RepeatedCompositeFieldContainer[_creator_application_pb2.CreatorApplication]
    def __init__(self, applicants: _Optional[_Iterable[_Union[_creator_application_pb2.CreatorApplication, _Mapping]]] = ...) -> None: ...

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

class QueryGetUnscoredSubmissionsByTaskRequest(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class QueryGetUnscoredSubmissionsByTaskResponse(_message.Message):
    __slots__ = ("submissions",)
    SUBMISSIONS_FIELD_NUMBER: _ClassVar[int]
    submissions: _containers.RepeatedCompositeFieldContainer[_submission_pb2.Submission]
    def __init__(self, submissions: _Optional[_Iterable[_Union[_submission_pb2.Submission, _Mapping]]] = ...) -> None: ...

class QueryCanTriggerFinalSubmissionRequest(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanTriggerFinalSubmissionResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanTriggerFinalTestingRequest(_message.Message):
    __slots__ = ("creator", "task_id")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    creator: str
    task_id: int
    def __init__(self, creator: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanTriggerFinalTestingResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanRegisterAsTrainerRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanRegisterAsTrainerResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanRegisterAsScorerRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanRegisterAsScorerResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryIsTrainerRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryIsTrainerResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryIsScorerRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryIsScorerResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanSubmitTrainingResultRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanSubmitTrainingResultResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanSubmitFinalResultRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanSubmitFinalResultResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryCanRequestScoringTaskRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryCanRequestScoringTaskResponse(_message.Message):
    __slots__ = ("result", "reason")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    result: bool
    reason: _error_code_pb2.ErrorCode
    def __init__(self, result: bool = ..., reason: _Optional[_Union[_error_code_pb2.ErrorCode, str]] = ...) -> None: ...

class QueryGetPendingScoringTasksRequest(_message.Message):
    __slots__ = ("user", "task_id")
    USER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    user: str
    task_id: int
    def __init__(self, user: _Optional[str] = ..., task_id: _Optional[int] = ...) -> None: ...

class QueryGetPendingScoringTasksResponse(_message.Message):
    __slots__ = ("score_tasks",)
    SCORE_TASKS_FIELD_NUMBER: _ClassVar[int]
    score_tasks: _containers.RepeatedCompositeFieldContainer[_score_task_pb2.ScoreTask]
    def __init__(self, score_tasks: _Optional[_Iterable[_Union[_score_task_pb2.ScoreTask, _Mapping]]] = ...) -> None: ...

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

class QueryGetPlagiarismReportFromUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...

class QueryGetPlagiarismReportFromUserResponse(_message.Message):
    __slots__ = ("plagiarism_reports",)
    PLAGIARISM_REPORTS_FIELD_NUMBER: _ClassVar[int]
    plagiarism_reports: _containers.RepeatedCompositeFieldContainer[_plagiarism_report_pb2.PlagiarismReport]
    def __init__(self, plagiarism_reports: _Optional[_Iterable[_Union[_plagiarism_report_pb2.PlagiarismReport, _Mapping]]] = ...) -> None: ...

class QueryGetScoreDisputeFromUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: str
    def __init__(self, user: _Optional[str] = ...) -> None: ...

class QueryGetScoreDisputeFromUserResponse(_message.Message):
    __slots__ = ("dispute_score_tasks",)
    DISPUTE_SCORE_TASKS_FIELD_NUMBER: _ClassVar[int]
    dispute_score_tasks: _containers.RepeatedCompositeFieldContainer[_dispute_score_task_pb2.DisputeScoreTask]
    def __init__(self, dispute_score_tasks: _Optional[_Iterable[_Union[_dispute_score_task_pb2.DisputeScoreTask, _Mapping]]] = ...) -> None: ...
