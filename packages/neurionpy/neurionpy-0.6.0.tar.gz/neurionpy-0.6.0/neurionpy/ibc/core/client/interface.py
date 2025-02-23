from abc import ABC, abstractmethod

from neurionpy.protos.ibc.core.client.v1.query_pb2 import (
    QueryClientParamsRequest,
    QueryClientParamsResponse,
    QueryClientStateRequest,
    QueryClientStateResponse,
    QueryClientStatesRequest,
    QueryClientStatesResponse,
    QueryConsensusStateRequest,
    QueryConsensusStateResponse,
    QueryConsensusStatesRequest,
    QueryConsensusStatesResponse,
)


class IBCCoreClient(ABC):
    """IBC Core Client abstract class."""

    @abstractmethod
    def ClientState(self, request: QueryClientStateRequest) -> QueryClientStateResponse:
        """
        ClientState queries an IBC light client.

        :param request: QueryClientStateRequest
        :return: QueryClientStateResponse
        """

    @abstractmethod
    def ClientStates(
        self, request: QueryClientStatesRequest
    ) -> QueryClientStatesResponse:
        """
        ClientStates queries all the IBC light clients of a chain.

        :param request: QueryClientStatesRequest
        :return: QueryClientStatesResponse
        """

    @abstractmethod
    def ConsensusState(
        self, request: QueryConsensusStateRequest
    ) -> QueryConsensusStateResponse:
        """
        ConsensusState queries a consensus state associated with a client state at a given height.

        :param request: QueryConsensusStateRequest
        :return: QueryConsensusStateResponse
        """

    @abstractmethod
    def ConsensusStates(
        self, request: QueryConsensusStatesRequest
    ) -> QueryConsensusStatesResponse:
        """
        ConsensusStates queries all the consensus states associated with a given client.

        :param request: QueryConsensusStatesRequest
        :return: QueryConsensusStatesResponse
        """

    @abstractmethod
    def ClientParams(
        self, request: QueryClientParamsRequest
    ) -> QueryClientParamsResponse:
        """
        ClientParams queries all parameters of the IBC client.

        :param request: QueryClientParamsRequest
        :return: QueryClientParamsResponse
        """
