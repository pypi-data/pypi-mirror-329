from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.fusion.query_pb2 import QueryParamsRequest, QueryParamsResponse
from neurionpy.synapse.tx_helpers import SubmittedTx
from neurionpy.synapse.wallet import Wallet


class FusionQuery(ABC):
    """Sanctum abstract class."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Query the parameters of bank module.
        :param request: QueryParamsRequest
        :return: QueryParamsResponse
        """


class FusionMessage(ABC):
    """Fusion abstract class."""


