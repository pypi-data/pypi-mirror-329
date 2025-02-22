from abc import ABC, abstractmethod

from neurionpy.protos.ibc.applications.transfer.v1.query_pb2 import (
    QueryDenomTraceRequest,
    QueryDenomTraceResponse,
    QueryDenomTracesRequest,
    QueryDenomTracesResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)


class IBCApplicationsTransfer(ABC):
    """IBC Applications Transfer abstract class."""

    @abstractmethod
    def DenomTrace(self, request: QueryDenomTraceRequest) -> QueryDenomTraceResponse:
        """
        DenomTrace queries a denomination trace information.

        :param request: QueryDenomTraceRequest
        :return: QueryDenomTraceResponse
        """

    @abstractmethod
    def DenomTraces(self, request: QueryDenomTracesRequest) -> QueryDenomTracesResponse:
        """
        DenomTraces queries all denomination traces.

        :param request: QueryDenomTracesRequest
        :return: QueryDenomTracesResponse
        """

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Params queries all parameters of the ibc-transfer module.

        :param request: QueryParamsRequest
        :return: QueryParamsResponse
        """
