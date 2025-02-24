from abc import ABC, abstractmethod

from neurionpy.protos.cosmos.upgrade.v1beta1.query_pb2 import (
    QueryAppliedPlanRequest,
    QueryAppliedPlanResponse,
    QueryCurrentPlanRequest,
    QueryCurrentPlanResponse,
)


class CosmosUpgrade(ABC):
    """Cosmos Upgrade abstract class."""

    @abstractmethod
    def CurrentPlan(self, request: QueryCurrentPlanRequest) -> QueryCurrentPlanResponse:
        """
        CurrentPlan queries the current upgrade plan.

        :param request: QueryCurrentPlanRequest
        :return: QueryCurrentPlanResponse
        """

    @abstractmethod
    def AppliedPlan(self, request: QueryAppliedPlanRequest) -> QueryAppliedPlanResponse:
        """
        AppliedPlan queries a previously applied upgrade plan by its name.

        :param request: QueryAppliedPlanRequest
        :return: QueryAppliedPlanResponse
        """
