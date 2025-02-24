from google.protobuf.json_format import Parse
from neurionpy.common.rest_client import RestClient
from neurionpy.protos.neurion.sanctum.query_pb2 import (
    QueryParamsRequest, QueryParamsResponse,
    QueryGetAvailableDatasetsRequest, QueryGetAvailableDatasetsResponse,
    QueryGetApprovedUsageRequestsRequest, QueryGetApprovedUsageRequestsResponse,
    QueryGetRewardRequest, QueryGetRewardResponse,
    QueryGetStakeRequest, QueryGetStakeResponse,
    QueryGetPendingDatasetsRequest, QueryGetPendingDatasetsResponse,
    QueryGetPendingUsageRequestsRequest, QueryGetPendingUsageRequestsResponse,
    QueryGetDatasetRequest, QueryGetDatasetResponse,
    QueryGetUsageRequestRequest, QueryGetUsageRequestResponse,
    QueryGetUsageRequestsForDatasetRequest, QueryGetUsageRequestsForDatasetResponse,
    QueryGetUsageRequestsForUserRequest, QueryGetUsageRequestsForUserResponse,
    QueryGetDatasetsForUserRequest, QueryGetDatasetsForUserResponse
)
from neurionpy.sanctum.interface import SanctumQuery

class SanctumRestClient(SanctumQuery):
    """Sanctum REST client implementing all query endpoints."""
    API_URL = "/neurion/sanctum"

    def __init__(self, rest_api: RestClient):
        """
        Create Sanctum REST client.

        :param rest_api: RestClient instance for making HTTP requests.
        """
        self._rest_api = rest_api

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(response, QueryParamsResponse())

    def GetAvailableDatasets(self, request: QueryGetAvailableDatasetsRequest) -> QueryGetAvailableDatasetsResponse:
        params = {"offset": request.offset, "limit": request.limit}
        response = self._rest_api.get(f"{self.API_URL}/get_available_datasets", params=params)
        return Parse(response, QueryGetAvailableDatasetsResponse())

    def GetApprovedUsageRequests(self, request: QueryGetApprovedUsageRequestsRequest) -> QueryGetApprovedUsageRequestsResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_approved_usage_requests")
        return Parse(response, QueryGetApprovedUsageRequestsResponse())

    def GetReward(self, request: QueryGetRewardRequest) -> QueryGetRewardResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_reward/{request.user}")
        return Parse(response, QueryGetRewardResponse())

    def GetStake(self, request: QueryGetStakeRequest) -> QueryGetStakeResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_stake/{request.user}")
        return Parse(response, QueryGetStakeResponse())

    def GetPendingDatasets(self, request: QueryGetPendingDatasetsRequest) -> QueryGetPendingDatasetsResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_pending_datasets")
        return Parse(response, QueryGetPendingDatasetsResponse())

    def GetPendingUsageRequests(self, request: QueryGetPendingUsageRequestsRequest) -> QueryGetPendingUsageRequestsResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_pending_usage_requests/{request.user}")
        return Parse(response, QueryGetPendingUsageRequestsResponse())

    def GetDataset(self, request: QueryGetDatasetRequest) -> QueryGetDatasetResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_dataset/{request.id}")
        return Parse(response, QueryGetDatasetResponse())

    def GetUsageRequest(self, request: QueryGetUsageRequestRequest) -> QueryGetUsageRequestResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_usage_request/{request.id}")
        return Parse(response, QueryGetUsageRequestResponse())

    def GetUsageRequestsForDataset(self, request: QueryGetUsageRequestsForDatasetRequest) -> QueryGetUsageRequestsForDatasetResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_usage_requests_for_dataset/{request.dataset_id}/{request.offset}/{request.limit}")
        return Parse(response, QueryGetUsageRequestsForDatasetResponse())

    def GetUsageRequestsForUser(self, request: QueryGetUsageRequestsForUserRequest) -> QueryGetUsageRequestsForUserResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_usage_requests_for_user/{request.user}/{request.offset}/{request.limit}")
        return Parse(response, QueryGetUsageRequestsForUserResponse())

    def GetDatasetsForUser(self, request: QueryGetDatasetsForUserRequest) -> QueryGetDatasetsForUserResponse:
        response = self._rest_api.get(f"{self.API_URL}/get_datasets_for_user/{request.user}/{request.offset}/{request.limit}")
        return Parse(response, QueryGetDatasetsForUserResponse())
