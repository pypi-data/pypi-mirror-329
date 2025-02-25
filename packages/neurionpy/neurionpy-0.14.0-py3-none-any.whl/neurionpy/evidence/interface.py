from abc import ABC, abstractmethod

from neurionpy.protos.cosmos.evidence.v1beta1.query_pb2 import (
    QueryAllEvidenceRequest,
    QueryAllEvidenceResponse,
    QueryEvidenceRequest,
    QueryEvidenceResponse,
)


class Evidence(ABC):
    """Evidence abstract class."""

    @abstractmethod
    def Evidence(self, request: QueryEvidenceRequest) -> QueryEvidenceResponse:
        """
        Evidence queries evidence based on evidence hash.

        :param request: QueryEvidenceRequest

        :return: QueryEvidenceResponse
        """

    @abstractmethod
    def AllEvidence(self, request: QueryAllEvidenceRequest) -> QueryAllEvidenceResponse:
        """
        AllEvidence queries all evidence.

        :param request: QueryAllEvidenceRequest

        :return: QueryAllEvidenceResponse
        """
