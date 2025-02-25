from abc import ABC, abstractmethod

from neurionpy.protos.cosmos.slashing.v1beta1.query_pb2 import (
    QueryParamsResponse,
    QuerySigningInfoRequest,
    QuerySigningInfoResponse,
    QuerySigningInfosRequest,
    QuerySigningInfosResponse,
)


class Slashing(ABC):
    """Slashing abstract class."""

    @abstractmethod
    def Params(self) -> QueryParamsResponse:
        """
        Params queries the parameters of slashing module.

        :return: QueryParamsResponse
        """

    @abstractmethod
    def SigningInfo(self, request: QuerySigningInfoRequest) -> QuerySigningInfoResponse:
        """
        SigningInfo queries the signing info of given cons address.

        :param request: QuerySigningInfoRequest

        :return: QuerySigningInfoResponse
        """

    @abstractmethod
    def SigningInfos(
        self, request: QuerySigningInfosRequest
    ) -> QuerySigningInfosResponse:
        """
        SigningInfos queries signing info of all validators.

        :param request: QuerySigningInfosRequest

        :return: QuerySigningInfosResponse
        """
