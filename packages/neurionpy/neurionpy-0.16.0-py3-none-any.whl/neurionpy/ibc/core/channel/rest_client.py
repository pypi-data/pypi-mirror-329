from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.ibc.core.channel.interface import IBCCoreChannel  # type: ignore
from neurionpy.protos.ibc.core.channel.v1.query_pb2 import (
    QueryChannelClientStateRequest,
    QueryChannelClientStateResponse,
    QueryChannelConsensusStateRequest,
    QueryChannelConsensusStateResponse,
    QueryChannelRequest,
    QueryChannelResponse,
    QueryChannelsRequest,
    QueryChannelsResponse,
    QueryConnectionChannelsRequest,
    QueryConnectionChannelsResponse,
    QueryNextSequenceReceiveRequest,
    QueryNextSequenceReceiveResponse,
    QueryPacketAcknowledgementRequest,
    QueryPacketAcknowledgementResponse,
    QueryPacketAcknowledgementsRequest,
    QueryPacketAcknowledgementsResponse,
    QueryPacketCommitmentRequest,
    QueryPacketCommitmentResponse,
    QueryPacketCommitmentsRequest,
    QueryPacketCommitmentsResponse,
    QueryPacketReceiptRequest,
    QueryPacketReceiptResponse,
    QueryUnreceivedAcksRequest,
    QueryUnreceivedAcksResponse,
    QueryUnreceivedPacketsRequest,
    QueryUnreceivedPacketsResponse,
)


class IBCCoreChannelRestClient(IBCCoreChannel):
    """IBC Core Channel REST client."""

    API_URL = "/ibc/core/channel/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Channel(self, request: QueryChannelRequest) -> QueryChannelResponse:
        """
        Channel queries an IBC Channel.

        :param request: QueryChannelRequest
        :return: QueryChannelResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}"
        )
        return Parse(json_response, QueryChannelResponse())

    def Channels(self, request: QueryChannelsRequest) -> QueryChannelsResponse:
        """
        Channels queries all the IBC channels of a chain.

        :param request: QueryChannelsRequest
        :return: QueryChannelsResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/channels", request)
        return Parse(json_response, QueryChannelsResponse())

    def ConnectionChannels(
        self, request: QueryConnectionChannelsRequest
    ) -> QueryConnectionChannelsResponse:
        """
        ConnectionChannels queries all the channels associated with a connection.

        :param request: QueryConnectionChannelsRequest
        :return: QueryConnectionChannelsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/connections/{request.connection}/channels", request
        )
        return Parse(json_response, QueryConnectionChannelsResponse())

    def ChannelClientState(
        self, request: QueryChannelClientStateRequest
    ) -> QueryChannelClientStateResponse:
        """
        ChannelClientState queries for the client state for the channel associated with the provided channel identifiers.

        :param request: QueryChannelClientStateRequest
        :return: QueryChannelClientStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/client_state"
        )
        return Parse(json_response, QueryChannelClientStateResponse())

    def ChannelConsensusState(
        self, request: QueryChannelConsensusStateRequest
    ) -> QueryChannelConsensusStateResponse:
        """
        ChannelConsensusState queries for the consensus state for the channel associated with the provided channel identifiers.

        :param request: QueryChannelConsensusStateRequest
        :return: QueryChannelConsensusStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/consensus_state/revision/{request.revision_number}/height/{request.revision_height}"
        )
        return Parse(json_response, QueryChannelConsensusStateResponse())

    def PacketCommitment(
        self, request: QueryPacketCommitmentRequest
    ) -> QueryPacketCommitmentResponse:
        """
        PacketCommitment queries a stored packet commitment hash.

        :param request: QueryPacketCommitmentRequest
        :return: QueryPacketCommitmentResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/packet_commitments/{request.sequence}"
        )
        return Parse(json_response, QueryPacketCommitmentResponse())

    def PacketCommitments(
        self, request: QueryPacketCommitmentsRequest
    ) -> QueryPacketCommitmentsResponse:
        """
        PacketCommitments returns all the packet commitments hashes associated with a channel.

        :param request: QueryPacketCommitmentsRequest
        :return: QueryPacketCommitmentsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/packet_commitments",
            request,
        )
        return Parse(json_response, QueryPacketCommitmentsResponse())

    def PacketReceipt(
        self, request: QueryPacketReceiptRequest
    ) -> QueryPacketReceiptResponse:
        """
        PacketReceipt queries if a given packet sequence has been received on the queried chain.

        :param request: QueryPacketReceiptRequest
        :return: QueryPacketReceiptResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/packet_receipts/{request.sequence}"
        )
        return Parse(json_response, QueryPacketReceiptResponse())

    def PacketAcknowledgement(
        self, request: QueryPacketAcknowledgementRequest
    ) -> QueryPacketAcknowledgementResponse:
        """
        PacketAcknowledgement queries a stored packet acknowledgment hash.

        :param request: QueryPacketAcknowledgementRequest
        :return: QueryPacketAcknowledgementResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/packet_acks/{request.sequence}"
        )
        return Parse(json_response, QueryPacketAcknowledgementResponse())

    def PacketAcknowledgements(
        self, request: QueryPacketAcknowledgementsRequest
    ) -> QueryPacketAcknowledgementsResponse:
        """
        PacketAcknowledgements returns all the packet acknowledgments associated with a channel.

        :param request: QueryPacketAcknowledgementsRequest
        :return: QueryPacketAcknowledgementsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/packet_acknowledgements",
            request,
        )
        return Parse(json_response, QueryPacketAcknowledgementsResponse())

    def UnreceivedPackets(
        self, request: QueryUnreceivedPacketsRequest
    ) -> QueryUnreceivedPacketsResponse:
        """
        UnreceivedPackets returns all the unreceived IBC packets associated with a channel and sequences.

        :param request: QueryUnreceivedPacketsRequest
        :return: QueryUnreceivedPacketsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/packet_commitments/{','.join(map(str,request.packet_commitment_sequences))}/unreceived_packets",
            request,
        )
        return Parse(json_response, QueryUnreceivedPacketsResponse())

    def UnreceivedAcks(
        self, request: QueryUnreceivedAcksRequest
    ) -> QueryUnreceivedAcksResponse:
        """
        UnreceivedAcks returns all the unreceived IBC acknowledgments associated with a channel and sequences.

        :param request: QueryUnreceivedAcksRequest
        :return: QueryUnreceivedAcksResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/packet_commitments/{','.join(map(str,request.packet_ack_sequences))}/unreceived_acks",
            request,
        )
        return Parse(json_response, QueryUnreceivedAcksResponse())

    def NextSequenceReceive(
        self, request: QueryNextSequenceReceiveRequest
    ) -> QueryNextSequenceReceiveResponse:
        """
        NextSequenceReceive returns the next receive sequence for a given channel.

        :param request: QueryNextSequenceReceiveRequest
        :return: QueryNextSequenceReceiveResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/channels/{request.channel_id}/ports/{request.port_id}/next_sequence"
        )
        return Parse(json_response, QueryNextSequenceReceiveResponse())
