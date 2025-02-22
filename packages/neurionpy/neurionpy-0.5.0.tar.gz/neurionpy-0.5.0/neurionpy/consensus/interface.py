from abc import ABC, abstractmethod

from neurionpy.protos.cosmos.consensus.v1.query_pb2 import QueryParamsRequest, QueryParamsResponse


class Consensus(ABC):
    """Consensus abstract class."""
    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Query the parameters of bank module.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """