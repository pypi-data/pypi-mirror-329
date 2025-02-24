from abc import ABC, abstractmethod

from neurionpy.protos.ibc.core.connection.v1.query_pb2 import (
    QueryClientConnectionsRequest,
    QueryClientConnectionsResponse,
    QueryConnectionClientStateRequest,
    QueryConnectionClientStateResponse,
    QueryConnectionConsensusStateRequest,
    QueryConnectionConsensusStateResponse,
    QueryConnectionRequest,
    QueryConnectionResponse,
    QueryConnectionsRequest,
    QueryConnectionsResponse,
)


class IBCCoreConnection(ABC):
    """IBC Core Connection abstract class."""

    @abstractmethod
    def Connection(self, request: QueryConnectionRequest) -> QueryConnectionResponse:
        """
        Connection queries an IBC connection end.

        :param request: QueryConnectionRequest
        :return: QueryConnectionResponse
        """  # noqa: D401

    @abstractmethod
    def Connections(self, request: QueryConnectionsRequest) -> QueryConnectionsResponse:
        """
        Connection queries all the IBC connections of a chain.

        :param request: QueryConnectionsRequest
        :return: QueryConnectionsResponse
        """  # noqa: D401

    @abstractmethod
    def ClientConnections(
        self, request: QueryClientConnectionsRequest
    ) -> QueryClientConnectionsResponse:
        """
        ClientConnection queries the connection paths associated with a client state.

        :param request: QueryClientConnectionsRequest
        :return: QueryClientConnectionsResponse
        """

    @abstractmethod
    def ConnectionClientState(
        self, request: QueryConnectionClientStateRequest
    ) -> QueryConnectionClientStateResponse:
        """
        ConnectionClientState queries the client state associated with the connection.

        :param request: QueryConnectionClientStateRequest
        :return: QueryConnectionClientStateResponse
        """

    @abstractmethod
    def ConnectionConsensusState(
        self, request: QueryConnectionConsensusStateRequest
    ) -> QueryConnectionConsensusStateResponse:
        """
        ConnectionConsensusState queries the consensus state associated with the connection.

        :param request: QueryConnectionConsensusStateRequest
        :return: QueryConnectionConsensusStateResponse
        """
