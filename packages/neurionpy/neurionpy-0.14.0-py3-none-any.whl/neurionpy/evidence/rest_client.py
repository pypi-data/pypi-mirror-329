
from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.evidence.interface import Evidence
from neurionpy.protos.cosmos.evidence.v1beta1.query_pb2 import (
    QueryAllEvidenceRequest,
    QueryAllEvidenceResponse,
    QueryEvidenceRequest,
    QueryEvidenceResponse,
)


class EvidenceRestClient(Evidence):
    """Evidence REST client."""

    API_URL = "/cosmos/evidence/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Evidence(self, request: QueryEvidenceRequest) -> QueryEvidenceResponse:
        """
        Evidence queries evidence based on evidence hash.

        :param request: QueryEvidenceRequest

        :return: QueryEvidenceResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/evidence/{request.evidence_hash}",
        )
        return Parse(json_response, QueryEvidenceResponse())

    def AllEvidence(self, request: QueryAllEvidenceRequest) -> QueryAllEvidenceResponse:
        """
        AllEvidence queries all evidence.

        :param request: QueryAllEvidenceRequest

        :return: QueryAllEvidenceResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/evidence", request)
        return Parse(json_response, QueryAllEvidenceResponse())
