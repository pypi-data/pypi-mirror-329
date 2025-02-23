from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.fusion.tx_pb2 import (
    MsgUpdateParams, MsgUpdateParamsResponse,
    MsgApplyCreator, MsgApplyCreatorResponse,
    MsgApproveApplication, MsgApproveApplicationResponse,
    MsgRejectApplication, MsgRejectApplicationResponse,
    MsgCreateTask, MsgCreateTaskResponse,
    MsgStartTask, MsgStartTaskResponse,
    MsgProposeModel, MsgProposeModelResponse,
    MsgRegisterProposer, MsgRegisterProposerResponse,
    MsgRegisterValidator, MsgRegisterValidatorResponse,
    MsgStartTesting, MsgStartTestingResponse,
    MsgRequestValidationTask, MsgRequestValidationTaskResponse,
    MsgSubmitScore, MsgSubmitScoreResponse,
    MsgDisputeModelScore, MsgDisputeModelScoreResponse,
    MsgStartNewRound, MsgStartNewRoundResponse,
    MsgTerminateTask, MsgTerminateTaskResponse,
    MsgStakeToTask, MsgStakeToTaskResponse,
    MsgClaimTaskReward, MsgClaimTaskRewardResponse,
    MsgUnstakeFromTask, MsgUnstakeFromTaskResponse,
    MsgDisclaimCreatorStatus, MsgDisclaimCreatorStatusResponse,
    MsgAbortTask, MsgAbortTaskResponse,
)

from neurionpy.protos.neurion.fusion.query_pb2 import (
    QueryParamsRequest, QueryParamsResponse,
    QueryGetTaskRequest, QueryGetTaskResponse,
    QueryGetTaskRewardRequest, QueryGetTaskRewardResponse,
    QueryGetCreatorApplicationsRequest, QueryGetCreatorApplicationsResponse,
    QueryGetPendingCreatorApplicationsRequest, QueryGetPendingCreatorApplicationsResponse,
    QueryGetModelsByRoundRequest, QueryGetModelsByRoundResponse,
    QueryGetTaskStakeRequest, QueryGetTaskStakeResponse,
    QueryGetValidationTaskRequest, QueryGetValidationTaskResponse,
    QueryCanTriggerTestingForRoundRequest, QueryCanTriggerTestingForRoundResponse,
    QueryCanStartNewRoundRequest, QueryCanStartNewRoundResponse,
    QueryCanRegisterAsProposerRequest, QueryCanRegisterAsProposerResponse,
    QueryCanRegisterAsValidatorRequest, QueryCanRegisterAsValidatorResponse,
    QueryIsProposerRequest, QueryIsProposerResponse,
    QueryIsValidatorRequest, QueryIsValidatorResponse,
    QueryCanProposeModelRequest, QueryCanProposeModelResponse,
    QueryCanRequestValidationTaskRequest, QueryCanRequestValidationTaskResponse,
    QueryGetPendingValidationTasksRequest, QueryGetPendingValidationTasksResponse,
    QueryCanTerminateRequest, QueryCanTerminateResponse, QueryGetScoreDisputeFromUserRequest,
    QueryGetScoreDisputeFromUserResponse
)
from neurionpy.synapse.tx_helpers import SubmittedTx


class FusionQuery(ABC):
    """FusionQuery defines the interface for querying data in the Fusion module."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Query module parameters."""

    @abstractmethod
    def GetTask(self, request: QueryGetTaskRequest) -> QueryGetTaskResponse:
        """Query a task by its ID."""

    @abstractmethod
    def GetTaskReward(self, request: QueryGetTaskRewardRequest) -> QueryGetTaskRewardResponse:
        """Query task reward for a given task and user."""

    @abstractmethod
    def GetCreatorApplications(self, request: QueryGetCreatorApplicationsRequest) -> QueryGetCreatorApplicationsResponse:
        """Query creator applications for a given creator."""

    @abstractmethod
    def GetPendingCreatorApplications(self, request: QueryGetPendingCreatorApplicationsRequest) -> QueryGetPendingCreatorApplicationsResponse:
        """Query pending creator applications."""

    @abstractmethod
    def GetModelsByRound(self, request: QueryGetModelsByRoundRequest) -> QueryGetModelsByRoundResponse:
        """Query proposed models for a given task and round."""

    @abstractmethod
    def GetTaskStake(self, request: QueryGetTaskStakeRequest) -> QueryGetTaskStakeResponse:
        """Query task stake for a given task and user."""

    @abstractmethod
    def GetValidationTask(self, request: QueryGetValidationTaskRequest) -> QueryGetValidationTaskResponse:
        """Query a validation task by its ID."""

    @abstractmethod
    def CanTriggerTestingForRound(self, request: QueryCanTriggerTestingForRoundRequest) -> QueryCanTriggerTestingForRoundResponse:
        """Check if a user can trigger testing for a specific round."""

    @abstractmethod
    def CanStartNewRound(self, request: QueryCanStartNewRoundRequest) -> QueryCanStartNewRoundResponse:
        """Check if a user can start a new round."""

    @abstractmethod
    def CanRegisterAsProposer(self, request: QueryCanRegisterAsProposerRequest) -> QueryCanRegisterAsProposerResponse:
        """Check if a user can register as a proposer."""

    @abstractmethod
    def CanRegisterAsValidator(self, request: QueryCanRegisterAsValidatorRequest) -> QueryCanRegisterAsValidatorResponse:
        """Check if a user can register as a validator."""

    @abstractmethod
    def IsProposer(self, request: QueryIsProposerRequest) -> QueryIsProposerResponse:
        """Check if a user is a proposer for a task."""

    @abstractmethod
    def IsValidator(self, request: QueryIsValidatorRequest) -> QueryIsValidatorResponse:
        """Check if a user is a validator for a task."""

    @abstractmethod
    def CanProposeModel(self, request: QueryCanProposeModelRequest) -> QueryCanProposeModelResponse:
        """Check if a user can propose a model."""

    @abstractmethod
    def CanRequestValidationTask(self, request: QueryCanRequestValidationTaskRequest) -> QueryCanRequestValidationTaskResponse:
        """Check if a user can request a validation task."""

    @abstractmethod
    def GetPendingValidationTasks(self, request: QueryGetPendingValidationTasksRequest) -> QueryGetPendingValidationTasksResponse:
        """Query pending validation tasks for a user and task."""

    @abstractmethod
    def CanTerminate(self, request: QueryCanTerminateRequest) -> QueryCanTerminateResponse:
        """Check if a task can be terminated by the creator."""

    @abstractmethod
    def GetScoreDisputeFromUser(self, request: QueryGetScoreDisputeFromUserRequest) -> QueryGetScoreDisputeFromUserResponse:
        """Queries a list of score disputes raised by a user."""


class FusionMessage(ABC):
    """FusionMessage defines the interface for executing transactions in the Fusion module."""

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
    def StartTask(self, message: MsgStartTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Start a task."""

    @abstractmethod
    def ProposeModel(self, message: MsgProposeModel, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Propose a model for a task."""

    @abstractmethod
    def RegisterProposer(self, message: MsgRegisterProposer, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Register as a proposer for a task."""

    @abstractmethod
    def RegisterValidator(self, message: MsgRegisterValidator, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Register as a validator for a task."""

    @abstractmethod
    def StartTesting(self, message: MsgStartTesting, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Start testing for a task."""

    @abstractmethod
    def RequestValidationTask(self, message: MsgRequestValidationTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Request a validation task."""

    @abstractmethod
    def SubmitScore(self, message: MsgSubmitScore, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Submit a score for a validation task."""

    @abstractmethod
    def DisputeModelScore(self, message: MsgDisputeModelScore, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Dispute a model score."""

    @abstractmethod
    def StartNewRound(self, message: MsgStartNewRound, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Start a new round for a task."""

    @abstractmethod
    def TerminateTask(self, message: MsgTerminateTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Terminate a task."""

    @abstractmethod
    def StakeToTask(self, message: MsgStakeToTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Stake tokens to a task."""

    @abstractmethod
    def ClaimTaskReward(self, message: MsgClaimTaskReward, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Claim reward for a task."""

    @abstractmethod
    def UnstakeFromTask(self, message: MsgUnstakeFromTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Unstake tokens from a task."""

    @abstractmethod
    def DisclaimCreatorStatus(self, message: MsgDisclaimCreatorStatus, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Disclaim creator status."""

    @abstractmethod
    def AbortTask(self, message: MsgAbortTask, memo: Optional[str] = None, gas_limit: Optional[int] = None) -> SubmittedTx:
        """Abort a task."""

