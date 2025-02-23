from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
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
    QueryCanTerminateRequest, QueryCanTerminateResponse,
    QueryGetScoreDisputeFromUserRequest, QueryGetScoreDisputeFromUserResponse
)
from neurionpy.fusion.interface import FusionQuery


class FusionRestClient(FusionQuery):
    """Fusion REST client implementing all query endpoints."""
    API_URL = "/neurion/fusion"

    def __init__(self, rest_api: RestClient):
        """
        Initialize the Fusion REST client.

        :param rest_api: RestClient instance for making HTTP GET requests.
        """
        self._rest_api = rest_api

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Query module parameters."""
        response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(response, QueryParamsResponse())

    def GetTask(self, request: QueryGetTaskRequest) -> QueryGetTaskResponse:
        """Query a task by its ID."""
        response = self._rest_api.get(f"{self.API_URL}/get_task/{request.task_id}")
        return Parse(response, QueryGetTaskResponse())

    def GetTaskReward(self, request: QueryGetTaskRewardRequest) -> QueryGetTaskRewardResponse:
        """Query task reward for a given task and user."""
        response = self._rest_api.get(f"{self.API_URL}/get_task_reward/{request.task_id}/{request.user}")
        return Parse(response, QueryGetTaskRewardResponse())

    def GetCreatorApplications(self, request: QueryGetCreatorApplicationsRequest) -> QueryGetCreatorApplicationsResponse:
        """Query creator applications for a given creator."""
        response = self._rest_api.get(f"{self.API_URL}/get_creator_applications/{request.creator}")
        return Parse(response, QueryGetCreatorApplicationsResponse())

    def GetPendingCreatorApplications(self, request: QueryGetPendingCreatorApplicationsRequest) -> QueryGetPendingCreatorApplicationsResponse:
        """Query pending creator applications."""
        response = self._rest_api.get(f"{self.API_URL}/get_pending_creator_applications")
        return Parse(response, QueryGetPendingCreatorApplicationsResponse())

    def GetModelsByRound(self, request: QueryGetModelsByRoundRequest) -> QueryGetModelsByRoundResponse:
        """Query proposed models for a given task and round."""
        response = self._rest_api.get(f"{self.API_URL}/get_models_by_round/{request.task_id}/{request.round}")
        return Parse(response, QueryGetModelsByRoundResponse())

    def GetTaskStake(self, request: QueryGetTaskStakeRequest) -> QueryGetTaskStakeResponse:
        """Query task stake for a given task and user."""
        response = self._rest_api.get(f"{self.API_URL}/get_task_stake/{request.task_id}/{request.user}")
        return Parse(response, QueryGetTaskStakeResponse())

    def GetValidationTask(self, request: QueryGetValidationTaskRequest) -> QueryGetValidationTaskResponse:
        """Query a validation task by its ID."""
        response = self._rest_api.get(f"{self.API_URL}/get_validation_task/{request.id}")
        return Parse(response, QueryGetValidationTaskResponse())

    def CanTriggerTestingForRound(self, request: QueryCanTriggerTestingForRoundRequest) -> QueryCanTriggerTestingForRoundResponse:
        """Check if a user can trigger testing for a specific round."""
        response = self._rest_api.get(f"{self.API_URL}/can_trigger_testing_for_round/{request.user}/{request.task_id}/{request.round}")
        return Parse(response, QueryCanTriggerTestingForRoundResponse())

    def CanStartNewRound(self, request: QueryCanStartNewRoundRequest) -> QueryCanStartNewRoundResponse:
        """Check if a user can start a new round."""
        response = self._rest_api.get(f"{self.API_URL}/can_start_new_round/{request.user}/{request.task_id}/{request.round}")
        return Parse(response, QueryCanStartNewRoundResponse())

    def CanRegisterAsProposer(self, request: QueryCanRegisterAsProposerRequest) -> QueryCanRegisterAsProposerResponse:
        """Check if a user can register as a proposer."""
        response = self._rest_api.get(f"{self.API_URL}/can_register_as_proposer/{request.user}/{request.task_id}")
        return Parse(response, QueryCanRegisterAsProposerResponse())

    def CanRegisterAsValidator(self, request: QueryCanRegisterAsValidatorRequest) -> QueryCanRegisterAsValidatorResponse:
        """Check if a user can register as a validator."""
        response = self._rest_api.get(f"{self.API_URL}/can_register_as_validator/{request.user}/{request.task_id}")
        return Parse(response, QueryCanRegisterAsValidatorResponse())

    def IsProposer(self, request: QueryIsProposerRequest) -> QueryIsProposerResponse:
        """Check if a user is a proposer for a task."""
        response = self._rest_api.get(f"{self.API_URL}/is_proposer/{request.user}/{request.task_id}")
        return Parse(response, QueryIsProposerResponse())

    def IsValidator(self, request: QueryIsValidatorRequest) -> QueryIsValidatorResponse:
        """Check if a user is a validator for a task."""
        response = self._rest_api.get(f"{self.API_URL}/is_validator/{request.user}/{request.task_id}")
        return Parse(response, QueryIsValidatorResponse())

    def CanProposeModel(self, request: QueryCanProposeModelRequest) -> QueryCanProposeModelResponse:
        """Check if a user can propose a model."""
        response = self._rest_api.get(f"{self.API_URL}/can_propose_model/{request.user}/{request.task_id}/{request.round}")
        return Parse(response, QueryCanProposeModelResponse())

    def CanRequestValidationTask(self, request: QueryCanRequestValidationTaskRequest) -> QueryCanRequestValidationTaskResponse:
        """Check if a user can request a validation task."""
        response = self._rest_api.get(f"{self.API_URL}/can_request_validation_task/{request.user}/{request.task_id}/{request.round}")
        return Parse(response, QueryCanRequestValidationTaskResponse())

    def GetPendingValidationTasks(self, request: QueryGetPendingValidationTasksRequest) -> QueryGetPendingValidationTasksResponse:
        """Query pending validation tasks for a user and task."""
        response = self._rest_api.get(f"{self.API_URL}/get_pending_validation_tasks/{request.user}/{request.task_id}")
        return Parse(response, QueryGetPendingValidationTasksResponse())

    def CanTerminate(self, request: QueryCanTerminateRequest) -> QueryCanTerminateResponse:
        """Check if a task can be terminated by the creator."""
        response = self._rest_api.get(f"{self.API_URL}/can_terminate/{request.creator}/{request.task_id}")
        return Parse(response, QueryCanTerminateResponse())

    def GetScoreDisputeFromUser(self, request: QueryGetScoreDisputeFromUserRequest) -> QueryGetScoreDisputeFromUserResponse:
        """Queries a list of score disputes raised by a user."""
        response = self._rest_api.get(f"{self.API_URL}/get_score_dispute_from_user/{request.user}")
        return Parse(response, QueryGetScoreDisputeFromUserResponse())