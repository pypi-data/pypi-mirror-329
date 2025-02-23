from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.ibc.applications.transfer.interface import (  # type: ignore
    IBCApplicationsTransfer,
)
from neurionpy.protos.ibc.applications.transfer.v1.query_pb2 import (
    QueryDenomTraceRequest,
    QueryDenomTraceResponse,
    QueryDenomTracesRequest,
    QueryDenomTracesResponse,
    QueryParamsRequest,
    QueryParamsResponse,
)


class IBCApplicationsTransferRestClient(IBCApplicationsTransfer):
    """IBC Applications Transfer REST client."""

    API_URL = "/ibc/applications/transfer/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def DenomTrace(self, request: QueryDenomTraceRequest) -> QueryDenomTraceResponse:
        """
        DenomTrace queries a denomination trace information.

        :param request: QueryDenomTraceRequest
        :return: QueryDenomTraceResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/denom_traces/{request.hash}"
        )
        return Parse(json_response, QueryDenomTraceResponse())

    def DenomTraces(self, request: QueryDenomTracesRequest) -> QueryDenomTracesResponse:
        """
        DenomTraces queries all denomination traces.

        :param request: QueryDenomTracesRequest
        :return: QueryDenomTracesResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/denom_traces", request)
        return Parse(json_response, QueryDenomTracesResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Params queries all parameters of the ibc-transfer module.

        :param request: QueryParamsRequest
        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(json_response, QueryParamsResponse())
