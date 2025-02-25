from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.crucible.tx_pb2 import (
    MsgUpdateParams, MsgApplyCreator, MsgApproveApplication, MsgRejectApplication, MsgCreateTask,
    MsgRegisterTrainer, MsgRegisterScorer, MsgSubmitTrainingResult, MsgStakeToTask,
    MsgRequestScoringTask, MsgSubmitScore, MsgSubmitFinalResult, MsgReportModelPlagiarism,
    MsgAcceptPlagiarismReport, MsgRejectPlagiarismReport, MsgDisputeSubmissionScore,
    MsgStartTask, MsgAbortTask, MsgTriggerTaskToFinalSubmission, MsgTriggerTaskToFinalTesting,
    MsgTerminateTask, MsgClaimTaskReward, MsgUnstakeFromTask, MsgDisclaimCreatorStatus
)
from neurionpy.synapse.tx_helpers import SubmittedTx

from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.crucible.query_pb2 import (
    QueryParamsRequest, QueryParamsResponse, QueryGetCreatorsRequest, QueryGetCreatorsResponse,
    QueryGetCreatorApplicationsRequest, QueryGetCreatorApplicationsResponse,
    QueryGetTaskRequest, QueryGetTaskResponse, QueryListAllTasksRequest, QueryListAllTasksResponse,
    QueryListTasksByStatusRequest, QueryListTasksByStatusResponse, QueryGetSubmissionRequest,
    QueryGetSubmissionResponse, QueryGetSubmissionByTaskCreatorRequest, QueryGetSubmissionByTaskCreatorResponse,
    QueryGetSubmissionByTaskRequest, QueryGetSubmissionByTaskResponse, QueryGetEncryptedProofOfOwnershipRequest,
    QueryGetEncryptedProofOfOwnershipResponse, QueryGetPlagiarismReportRequest, QueryGetPlagiarismReportResponse,
    QueryGetTaskRewardRequest, QueryGetTaskRewardResponse, QueryGetPendingCreatorApplicationsRequest,
    QueryGetPendingCreatorApplicationsResponse, QueryGetTaskStakeRequest, QueryGetTaskStakeResponse,
    QueryGetUnscoredSubmissionsByTaskRequest, QueryGetUnscoredSubmissionsByTaskResponse,
    QueryCanTriggerFinalSubmissionRequest, QueryCanTriggerFinalSubmissionResponse,
    QueryCanTriggerFinalTestingRequest, QueryCanTriggerFinalTestingResponse,
    QueryCanRegisterAsTrainerRequest, QueryCanRegisterAsTrainerResponse,
    QueryCanRegisterAsScorerRequest, QueryCanRegisterAsScorerResponse,
    QueryIsTrainerRequest, QueryIsTrainerResponse, QueryIsScorerRequest, QueryIsScorerResponse,
    QueryCanSubmitTrainingResultRequest, QueryCanSubmitTrainingResultResponse,
    QueryCanSubmitFinalResultRequest, QueryCanSubmitFinalResultResponse,
    QueryCanRequestScoringTaskRequest, QueryCanRequestScoringTaskResponse,
    QueryGetPendingScoringTasksRequest, QueryGetPendingScoringTasksResponse,
    QueryCanTerminateRequest, QueryCanTerminateResponse, QueryGetPlagiarismReportFromUserRequest,
    QueryGetPlagiarismReportFromUserResponse, QueryGetScoreDisputeFromUserRequest, QueryGetScoreDisputeFromUserResponse
)


class CrucibleQuery(ABC):
    """Crucible abstract class defining query methods."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Query module parameters."""

    @abstractmethod
    def GetCreators(self, request: QueryGetCreatorsRequest) -> QueryGetCreatorsResponse:
        """Query the list of creators."""

    @abstractmethod
    def GetCreatorApplications(self, request: QueryGetCreatorApplicationsRequest) -> QueryGetCreatorApplicationsResponse:
        """Query creator applications for a given creator."""

    @abstractmethod
    def GetTask(self, request: QueryGetTaskRequest) -> QueryGetTaskResponse:
        """Query a task by its ID."""

    @abstractmethod
    def ListAllTasks(self, request: QueryListAllTasksRequest) -> QueryListAllTasksResponse:
        """Query all tasks with pagination."""

    @abstractmethod
    def ListTasksByStatus(self, request: QueryListTasksByStatusRequest) -> QueryListTasksByStatusResponse:
        """Query tasks by status with pagination."""

    @abstractmethod
    def GetSubmission(self, request: QueryGetSubmissionRequest) -> QueryGetSubmissionResponse:
        """Query a submission by its ID."""

    @abstractmethod
    def GetSubmissionByTask(self, request: QueryGetSubmissionByTaskRequest) -> QueryGetSubmissionByTaskResponse:
        """Query submissions by task ID."""

    @abstractmethod
    def GetSubmissionByTaskCreator(self, request: QueryGetSubmissionByTaskCreatorRequest) -> QueryGetSubmissionByTaskCreatorResponse:
        """Query a submission by task ID and creator."""

    @abstractmethod
    def GetEncryptedProofOfOwnership(self, request: QueryGetEncryptedProofOfOwnershipRequest) -> QueryGetEncryptedProofOfOwnershipResponse:
        """Query encrypted proof of ownership for a given key and plaintext."""

    @abstractmethod
    def GetPlagiarismReport(self, request: QueryGetPlagiarismReportRequest) -> QueryGetPlagiarismReportResponse:
        """Query a plagiarism report by report ID."""

    @abstractmethod
    def GetTaskReward(self, request: QueryGetTaskRewardRequest) -> QueryGetTaskRewardResponse:
        """Query task reward for a given task and user."""

    @abstractmethod
    def GetPendingCreatorApplications(self, request: QueryGetPendingCreatorApplicationsRequest) -> QueryGetPendingCreatorApplicationsResponse:
        """Query pending creator applications."""

    @abstractmethod
    def GetTaskStake(self, request: QueryGetTaskStakeRequest) -> QueryGetTaskStakeResponse:
        """Query task stake for a given task and user."""

    @abstractmethod
    def GetUnscoredSubmissionsByTask(self, request: QueryGetUnscoredSubmissionsByTaskRequest) -> QueryGetUnscoredSubmissionsByTaskResponse:
        """Query unscored submissions for a given task."""

    @abstractmethod
    def CanTriggerFinalSubmission(self, request: QueryCanTriggerFinalSubmissionRequest) -> QueryCanTriggerFinalSubmissionResponse:
        """Check if a user can trigger final submission for a task."""

    @abstractmethod
    def CanTriggerFinalTesting(self, request: QueryCanTriggerFinalTestingRequest) -> QueryCanTriggerFinalTestingResponse:
        """Check if a user can trigger final testing for a task."""

    @abstractmethod
    def CanRegisterAsTrainer(self, request: QueryCanRegisterAsTrainerRequest) -> QueryCanRegisterAsTrainerResponse:
        """Check if a user can register as a trainer."""

    @abstractmethod
    def CanRegisterAsScorer(self, request: QueryCanRegisterAsScorerRequest) -> QueryCanRegisterAsScorerResponse:
        """Check if a user can register as a scorer."""

    @abstractmethod
    def IsTrainer(self, request: QueryIsTrainerRequest) -> QueryIsTrainerResponse:
        """Check if a user is a trainer for a task."""

    @abstractmethod
    def IsScorer(self, request: QueryIsScorerRequest) -> QueryIsScorerResponse:
        """Check if a user is a scorer for a task."""

    @abstractmethod
    def CanSubmitTrainingResult(self, request: QueryCanSubmitTrainingResultRequest) -> QueryCanSubmitTrainingResultResponse:
        """Check if a user can submit a training result."""

    @abstractmethod
    def CanSubmitFinalResult(self, request: QueryCanSubmitFinalResultRequest) -> QueryCanSubmitFinalResultResponse:
        """Check if a user can submit the final result for a task."""

    @abstractmethod
    def CanRequestScoringTask(self, request: QueryCanRequestScoringTaskRequest) -> QueryCanRequestScoringTaskResponse:
        """Check if a user can request a scoring task."""

    @abstractmethod
    def GetPendingScoringTasks(self, request: QueryGetPendingScoringTasksRequest) -> QueryGetPendingScoringTasksResponse:
        """Query pending scoring tasks for a user and task."""

    @abstractmethod
    def CanTerminate(self, request: QueryCanTerminateRequest) -> QueryCanTerminateResponse:
        """Check if a task can be terminated by the creator."""

    @abstractmethod
    def GetPlagiarismReportFromUser(self, request: QueryGetPlagiarismReportFromUserRequest) -> QueryGetPlagiarismReportFromUserResponse:
        """Queries a list of plagiarism reports submitted by a specific user."""

    @abstractmethod
    def GetScoreDisputeFromUser(self, request: QueryGetScoreDisputeFromUserRequest) -> QueryGetScoreDisputeFromUserResponse:
        """Queries a list of score disputes raised by a specific user."""


class CrucibleMessage(ABC):
    """Crucible abstract class defining transaction messages."""

    @abstractmethod
    def UpdateParams(self, message: MsgUpdateParams, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Update module parameters."""

    @abstractmethod
    def ApplyCreator(self, message: MsgApplyCreator, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Apply to become a creator."""

    @abstractmethod
    def ApproveApplication(self, message: MsgApproveApplication, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Approve a creator application."""

    @abstractmethod
    def RejectApplication(self, message: MsgRejectApplication, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Reject a creator application."""

    @abstractmethod
    def CreateTask(self, message: MsgCreateTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Create a new task."""

    @abstractmethod
    def RegisterTrainer(self, message: MsgRegisterTrainer, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Register as a trainer for a task."""

    @abstractmethod
    def RegisterScorer(self, message: MsgRegisterScorer, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Register as a scorer for a task."""

    @abstractmethod
    def SubmitTrainingResult(self, message: MsgSubmitTrainingResult, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Submit a training result for a task."""

    @abstractmethod
    def StakeToTask(self, message: MsgStakeToTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Stake tokens to a task."""

    @abstractmethod
    def RequestScoringTask(self, message: MsgRequestScoringTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Request scoring for a task."""

    @abstractmethod
    def SubmitScore(self, message: MsgSubmitScore, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Submit a score for a scoring task."""

    @abstractmethod
    def SubmitFinalResult(self, message: MsgSubmitFinalResult, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Submit the final result for a task."""

    @abstractmethod
    def ReportModelPlagiarism(self, message: MsgReportModelPlagiarism, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Report model plagiarism."""

    @abstractmethod
    def AcceptPlagiarismReport(self, message: MsgAcceptPlagiarismReport, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Accept a plagiarism report."""

    @abstractmethod
    def RejectPlagiarismReport(self, message: MsgRejectPlagiarismReport, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Reject a plagiarism report."""

    @abstractmethod
    def DisputeSubmissionScore(self, message: MsgDisputeSubmissionScore, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Dispute a submission score."""

    @abstractmethod
    def StartTask(self, message: MsgStartTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Start a task."""

    @abstractmethod
    def AbortTask(self, message: MsgAbortTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Abort a task."""

    @abstractmethod
    def TriggerTaskToFinalSubmission(self, message: MsgTriggerTaskToFinalSubmission, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Trigger task transition to final submission phase."""

    @abstractmethod
    def TriggerTaskToFinalTesting(self, message: MsgTriggerTaskToFinalTesting, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Trigger task transition to final testing phase."""

    @abstractmethod
    def TerminateTask(self, message: MsgTerminateTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Terminate a task."""

    @abstractmethod
    def ClaimTaskReward(self, message: MsgClaimTaskReward, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Claim reward for a task."""

    @abstractmethod
    def UnstakeFromTask(self, message: MsgUnstakeFromTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Unstake tokens from a task."""

    @abstractmethod
    def DisclaimCreatorStatus(self, message: MsgDisclaimCreatorStatus, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Disclaim creator status."""