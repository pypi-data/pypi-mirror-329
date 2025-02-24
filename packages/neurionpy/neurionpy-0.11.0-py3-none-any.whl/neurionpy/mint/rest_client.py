import base64
import json
from typing import Union

from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.common.utils import json_encode
from neurionpy.mint.interface import Mint
from neurionpy.protos.cosmos.mint.v1beta1.query_pb2 import (
    QueryAnnualProvisionsResponse,
    QueryInflationResponse,
    QueryParamsResponse,
)


def isNumber(value: Union[str, bytes]) -> bool:
    """
    Check is string ob bytes is number.

    :param value: str, bytes
    :return: bool
    """
    try:
        float(str(value))
        return True
    except ValueError:
        return False


class MintRestClient(Mint):
    """Mint REST client."""

    API_URL = "/cosmos/mint/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def AnnualProvisions(self) -> QueryAnnualProvisionsResponse:
        """
        AnnualProvisions current minting annual provisions value.

        :return: a QueryAnnualProvisionsResponse instance
        """
        json_response = self._rest_api.get(f"{self.API_URL}/annual_provisions")
        # The QueryAnnualProvisionsResponse expect a base64 encoded value
        # but the Rest endpoint return digits
        j = json.loads(json_response)
        if isNumber(j["annual_provisions"]):
            j["annual_provisions"] = base64.b64encode(
                j["annual_provisions"].encode()
            ).decode("utf8")
        json_response = json_encode(j).encode("utf-8")

        return Parse(json_response, QueryAnnualProvisionsResponse())

    def Inflation(self) -> QueryInflationResponse:
        """
        Inflation returns the current minting inflation value.

        :return: a QueryInflationResponse instance
        """
        json_response = self._rest_api.get(f"{self.API_URL}/inflation")
        # The QueryInflationResponse expect a base64 encoded value
        # but the Rest endpoint return digits
        j = json.loads(json_response)
        if isNumber(j["inflation"]):
            j["inflation"] = base64.b64encode(j["inflation"].encode()).decode("utf8")
        json_response = json_encode(j).encode("utf-8")

        return Parse(json_response, QueryInflationResponse())

    def Params(self) -> QueryParamsResponse:
        """
        Params queries params of the Mint module.

        :return: a QueryParamsResponse instance
        """
        json_response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(json_response, QueryParamsResponse())
