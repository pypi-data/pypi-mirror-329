from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.crucible.query_pb2 import QueryParamsRequest, QueryParamsResponse
from neurionpy.synapse.tx_helpers import SubmittedTx


class CrucibleQuery(ABC):
    """Crucible abstract class."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Query the parameters of bank module.
        :param request: QueryParamsRequest
        :return: QueryParamsResponse
        """


class CrucibleMessage(ABC):
    """Crucible abstract class."""


