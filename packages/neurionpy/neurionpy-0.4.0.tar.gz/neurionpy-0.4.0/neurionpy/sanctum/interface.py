from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.sanctum.query_pb2 import QueryParamsRequest, QueryParamsResponse
from neurionpy.protos.neurion.sanctum.tx_pb2 import MsgSubmitDatasetApplication, MsgSubmitDatasetApplicationResponse
from neurionpy.synapse.tx_helpers import SubmittedTx
from neurionpy.synapse.wallet import Wallet


class SanctumQuery(ABC):
    """Sanctum abstract class."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Query the parameters of bank module.
        :param request: QueryParamsRequest
        :return: QueryParamsResponse
        """


class SanctumMessage(ABC):
    """Sanctum abstract class."""

    @abstractmethod
    def SubmitDatasetApplication(self, message: MsgSubmitDatasetApplication,
                                 memo: Optional[str] = None,
                                 gas_limit: Optional[int] = None) -> SubmittedTx:
        """
        Submit dataset application.
        :param message: MsgSubmitDatasetApplication
        :param memo: Optional[str]
        :param gas_limit: Optional[int]
        :raises RuntimeError: If unable to parse the value
        :return: SubmittedTx
        """
