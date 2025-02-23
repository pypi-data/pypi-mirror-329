from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.params.interface import Params
from neurionpy.protos.cosmos.params.v1beta1.query_pb2 import (
    QueryParamsRequest,
    QueryParamsResponse,
)


class ParamsRestClient(Params):
    """Params REST client."""

    API_URL = "/cosmos/params/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Params queries a specific Cosmos SDK parameter.

        :param request: QueryParamsRequest
        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/params", request)
        return Parse(json_response, QueryParamsResponse())
