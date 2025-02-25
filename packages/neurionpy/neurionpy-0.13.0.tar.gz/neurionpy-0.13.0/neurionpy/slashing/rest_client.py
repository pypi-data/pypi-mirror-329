from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.protos.cosmos.slashing.v1beta1.query_pb2 import (
    QueryParamsResponse,
    QuerySigningInfoRequest,
    QuerySigningInfoResponse,
    QuerySigningInfosRequest,
    QuerySigningInfosResponse,
)
from neurionpy.slashing.interface import Slashing


class SlashingRestClient(Slashing):
    """Slashing REST client."""

    API_URL = "/cosmos/slashing/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Params(self) -> QueryParamsResponse:
        """
        Params queries the parameters of slashing module.

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/params",
        )
        return Parse(json_response, QueryParamsResponse())

    def SigningInfo(self, request: QuerySigningInfoRequest) -> QuerySigningInfoResponse:
        """
        SigningInfo queries the signing info of given cons address.

        :param request: QuerySigningInfoRequest

        :return: QuerySigningInfoResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/signing_infos/{request.cons_address}",
        )
        return Parse(json_response, QuerySigningInfoResponse())

    def SigningInfos(
        self, request: QuerySigningInfosRequest
    ) -> QuerySigningInfosResponse:
        """
        SigningInfos queries signing info of all validators.

        :param request: QuerySigningInfosRequest

        :return: QuerySigningInfosResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/signing_infos", request)
        return Parse(json_response, QuerySigningInfosResponse())
