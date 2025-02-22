from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.consensus.interface import Consensus
from neurionpy.protos.cosmos.consensus.v1.query_pb2 import QueryParamsRequest, QueryParamsResponse


class ConsensusRestClient(Consensus):
    """Bank REST client."""

    API_URL = "/cosmos/consensus/v1"

    def __init__(self, rest_api: RestClient):
        """
        Create bank rest client.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Query the parameters of bank module.

        :param request: QueryParamsRequest

        :return: QueryParamsResponse
        """
        response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(response, QueryParamsResponse())