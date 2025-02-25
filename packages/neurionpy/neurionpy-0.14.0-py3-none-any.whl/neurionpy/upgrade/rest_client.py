from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.protos.cosmos.upgrade.v1beta1.query_pb2 import (
    QueryAppliedPlanRequest,
    QueryAppliedPlanResponse,
    QueryCurrentPlanRequest,
    QueryCurrentPlanResponse,
)
from neurionpy.upgrade.interface import CosmosUpgrade


class CosmosUpgradeRestClient(CosmosUpgrade):
    """Cosmos Upgrade REST client."""

    API_URL = "/cosmos/upgrade/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def CurrentPlan(self, request: QueryCurrentPlanRequest) -> QueryCurrentPlanResponse:
        """
        CurrentPlan queries the current upgrade plan.

        :param request: QueryCurrentPlanRequest
        :return: QueryCurrentPlanResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/current_plan",
        )
        return Parse(json_response, QueryCurrentPlanResponse())

    def AppliedPlan(self, request: QueryAppliedPlanRequest) -> QueryAppliedPlanResponse:
        """
        AppliedPlan queries a previously applied upgrade plan by its name.

        :param request: QueryAppliedPlanRequest
        :return: QueryAppliedPlanResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/applied_plan/{request.name}", request
        )
        return Parse(json_response, QueryAppliedPlanResponse())
