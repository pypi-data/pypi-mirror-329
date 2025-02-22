from abc import ABC, abstractmethod

from neurionpy.protos.cosmos.mint.v1beta1.query_pb2 import (
    QueryAnnualProvisionsResponse,
    QueryInflationResponse,
    QueryParamsResponse,
)


class Mint(ABC):
    """Mint abstract class."""

    @abstractmethod
    def AnnualProvisions(self) -> QueryAnnualProvisionsResponse:
        """
        AnnualProvisions current minting annual provisions value.

        :return: a QueryAnnualProvisionsResponse instance
        """

    @abstractmethod
    def Inflation(self) -> QueryInflationResponse:
        """
        Inflation returns the current minting inflation value.

        :return: a QueryInflationResponse instance
        """

    @abstractmethod
    def Params(self) -> QueryParamsResponse:
        """
        Params returns the total set of minting parameters.

        :return: QueryParamsResponse
        """
