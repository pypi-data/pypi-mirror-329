from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.protos.neurion.crucible.query_pb2 import (
    QueryParamsRequest, QueryParamsResponse,
    QueryGetCreatorsRequest, QueryGetCreatorsResponse,
    QueryGetCreatorApplicationsRequest, QueryGetCreatorApplicationsResponse,
    QueryGetTaskRequest, QueryGetTaskResponse,
    QueryListAllTasksRequest, QueryListAllTasksResponse,
    QueryListTasksByStatusRequest, QueryListTasksByStatusResponse,
    QueryGetSubmissionRequest, QueryGetSubmissionResponse,
    QueryGetSubmissionByTaskCreatorRequest, QueryGetSubmissionByTaskCreatorResponse,
    QueryGetSubmissionByTaskRequest, QueryGetSubmissionByTaskResponse,
    QueryGetEncryptedProofOfOwnershipRequest, QueryGetEncryptedProofOfOwnershipResponse,
    QueryGetPlagiarismReportRequest, QueryGetPlagiarismReportResponse,
    QueryGetTaskRewardRequest, QueryGetTaskRewardResponse,
    QueryGetPendingCreatorApplicationsRequest, QueryGetPendingCreatorApplicationsResponse,
    QueryGetTaskStakeRequest, QueryGetTaskStakeResponse,
    QueryGetUnscoredSubmissionsByTaskRequest, QueryGetUnscoredSubmissionsByTaskResponse,
    QueryCanTriggerFinalSubmissionRequest, QueryCanTriggerFinalSubmissionResponse,
    QueryCanTriggerFinalTestingRequest, QueryCanTriggerFinalTestingResponse,
    QueryCanRegisterAsTrainerRequest, QueryCanRegisterAsTrainerResponse,
    QueryCanRegisterAsScorerRequest, QueryCanRegisterAsScorerResponse,
    QueryIsTrainerRequest, QueryIsTrainerResponse,
    QueryIsScorerRequest, QueryIsScorerResponse,
    QueryCanSubmitTrainingResultRequest, QueryCanSubmitTrainingResultResponse,
    QueryCanSubmitFinalResultRequest, QueryCanSubmitFinalResultResponse,
    QueryCanRequestScoringTaskRequest, QueryCanRequestScoringTaskResponse,
    QueryGetPendingScoringTasksRequest, QueryGetPendingScoringTasksResponse,
    QueryCanTerminateRequest, QueryCanTerminateResponse,
    QueryGetPlagiarismReportFromUserRequest, QueryGetPlagiarismReportFromUserResponse,
    QueryGetScoreDisputeFromUserRequest, QueryGetScoreDisputeFromUserResponse
)
from neurionpy.crucible.interface import CrucibleQuery


class CrucibleRestClient(CrucibleQuery):
    """Crucible REST client implementing all query endpoints."""
    API_URL = "/neurion/crucible"

    def __init__(self, rest_api: RestClient):
        """
        Initialize the Crucible REST client.

        :param rest_api: RestClient instance for making HTTP requests.
        """
        self._rest_api = rest_api

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(response, QueryParamsResponse())

    def GetCreators(self, request: QueryGetCreatorsRequest) -> QueryGetCreatorsResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_creators")
        return Parse(response, QueryGetCreatorsResponse())

    def GetCreatorApplications(self, request: QueryGetCreatorApplicationsRequest) -> QueryGetCreatorApplicationsResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_creator_applications/{request.creator}")
        return Parse(response, QueryGetCreatorApplicationsResponse())

    def GetTask(self, request: QueryGetTaskRequest) -> QueryGetTaskResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_task/{request.id}")
        return Parse(response, QueryGetTaskResponse())

    def ListAllTasks(self, request: QueryListAllTasksRequest) -> QueryListAllTasksResponse:
        response = self._rest_api.get(f"{self.API_URL}/list_all_tasks/{request.offset}/{request.limit}")
        return Parse(response, QueryListAllTasksResponse())

    def ListTasksByStatus(self, request: QueryListTasksByStatusRequest) -> QueryListTasksByStatusResponse:
        response = self._rest_api.get(f"{self.API_URL}/list_tasks_by_status/{request.status}/{request.offset}/{request.limit}")
        return Parse(response, QueryListTasksByStatusResponse())

    def GetSubmission(self, request: QueryGetSubmissionRequest) -> QueryGetSubmissionResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_submission/{request.id}")
        return Parse(response, QueryGetSubmissionResponse())

    def GetSubmissionByTask(self, request: QueryGetSubmissionByTaskRequest) -> QueryGetSubmissionByTaskResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_submission_by_task/{request.task_id}")
        return Parse(response, QueryGetSubmissionByTaskResponse())

    def CanTriggerFinalSubmission(self, request: QueryCanTriggerFinalSubmissionRequest) -> QueryCanTriggerFinalSubmissionResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_trigger_final_submission/{request.creator}/{request.task_id}")
        return Parse(response, QueryCanTriggerFinalSubmissionResponse())

    def CanRegisterAsTrainer(self, request: QueryCanRegisterAsTrainerRequest) -> QueryCanRegisterAsTrainerResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_register_as_trainer/{request.user}/{request.task_id}")
        return Parse(response, QueryCanRegisterAsTrainerResponse())

    def CanSubmitTrainingResult(self, request: QueryCanSubmitTrainingResultRequest) -> QueryCanSubmitTrainingResultResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_submit_training_result/{request.user}/{request.task_id}")
        return Parse(response, QueryCanSubmitTrainingResultResponse())

    def GetPendingScoringTasks(self, request: QueryGetPendingScoringTasksRequest) -> QueryGetPendingScoringTasksResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_pending_scoring_tasks/{request.user}/{request.task_id}")
        return Parse(response, QueryGetPendingScoringTasksResponse())

    def CanTerminate(self, request: QueryCanTerminateRequest) -> QueryCanTerminateResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_terminate/{request.creator}/{request.task_id}")
        return Parse(response, QueryCanTerminateResponse())

    def GetSubmissionByTaskCreator(self, request: QueryGetSubmissionByTaskCreatorRequest) -> QueryGetSubmissionByTaskCreatorResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_submission_by_task_creator/{request.task_id}/{request.creator}")
        return Parse(response, QueryGetSubmissionByTaskCreatorResponse())

    def GetEncryptedProofOfOwnership(self, request: QueryGetEncryptedProofOfOwnershipRequest) -> QueryGetEncryptedProofOfOwnershipResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_encrypted_proof_of_ownership/{request.key}/{request.plaintext}")
        return Parse(response, QueryGetEncryptedProofOfOwnershipResponse())

    def GetPlagiarismReport(self, request: QueryGetPlagiarismReportRequest) -> QueryGetPlagiarismReportResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_plagiarism_report/{request.report_id}")
        return Parse(response, QueryGetPlagiarismReportResponse())

    def GetTaskReward(self, request: QueryGetTaskRewardRequest) -> QueryGetTaskRewardResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_task_reward/{request.task_id}/{request.user}")
        return Parse(response, QueryGetTaskRewardResponse())

    def GetPendingCreatorApplications(self, request: QueryGetPendingCreatorApplicationsRequest) -> QueryGetPendingCreatorApplicationsResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_pending_creator_applications")
        return Parse(response, QueryGetPendingCreatorApplicationsResponse())

    def GetTaskStake(self, request: QueryGetTaskStakeRequest) -> QueryGetTaskStakeResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_task_stake/{request.task_id}/{request.user}")
        return Parse(response, QueryGetTaskStakeResponse())

    def GetUnscoredSubmissionsByTask(self, request: QueryGetUnscoredSubmissionsByTaskRequest) -> QueryGetUnscoredSubmissionsByTaskResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_unscored_submissions_by_task/{request.task_id}")
        return Parse(response, QueryGetUnscoredSubmissionsByTaskResponse())

    def CanTriggerFinalTesting(self, request: QueryCanTriggerFinalTestingRequest) -> QueryCanTriggerFinalTestingResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_trigger_final_testing/{request.creator}/{request.task_id}")
        return Parse(response, QueryCanTriggerFinalTestingResponse())

    def CanRegisterAsScorer(self, request: QueryCanRegisterAsScorerRequest) -> QueryCanRegisterAsScorerResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_register_as_scorer/{request.user}/{request.task_id}")
        return Parse(response, QueryCanRegisterAsScorerResponse())

    def IsTrainer(self, request: QueryIsTrainerRequest) -> QueryIsTrainerResponse:
        response = self._rest_api.get(f"{self.API_URL}/is_trainer/{request.user}/{request.task_id}")
        return Parse(response, QueryIsTrainerResponse())

    def IsScorer(self, request: QueryIsScorerRequest) -> QueryIsScorerResponse:
        response = self._rest_api.get(f"{self.API_URL}/is_scorer/{request.user}/{request.task_id}")
        return Parse(response, QueryIsScorerResponse())

    def CanSubmitFinalResult(self, request: QueryCanSubmitFinalResultRequest) -> QueryCanSubmitFinalResultResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_submit_final_result/{request.user}/{request.task_id}")
        return Parse(response, QueryCanSubmitFinalResultResponse())

    def CanRequestScoringTask(self, request: QueryCanRequestScoringTaskRequest) -> QueryCanRequestScoringTaskResponse:
        response = self._rest_api.get(f"{self.API_URL}/can_request_scoring_task/{request.user}/{request.task_id}")
        return Parse(response, QueryCanRequestScoringTaskResponse())

    def GetPlagiarismReportFromUser(self, request: QueryGetPlagiarismReportFromUserRequest) -> QueryGetPlagiarismReportFromUserResponse:
        """Queries a list of plagiarism reports submitted by a specific user."""
        response = self._rest_api.get(f"{self.API_URL}/get_plagiarism_report_from_user/{request.user}")
        return Parse(response, QueryGetPlagiarismReportFromUserResponse())

    def GetScoreDisputeFromUser(self, request: QueryGetScoreDisputeFromUserRequest) -> QueryGetScoreDisputeFromUserResponse:
        """Queries a list of score disputes raised by a specific user."""
        response = self._rest_api.get(f"{self.API_URL}/get_score_dispute_from_user/{request.user}")
        return Parse(response, QueryGetScoreDisputeFromUserResponse())
