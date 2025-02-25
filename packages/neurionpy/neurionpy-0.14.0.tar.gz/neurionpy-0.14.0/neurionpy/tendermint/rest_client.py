from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.protos.cosmos.base.tendermint.v1beta1.query_pb2 import (
    GetBlockByHeightRequest,
    GetBlockByHeightResponse,
    GetLatestBlockRequest,
    GetLatestBlockResponse,
    GetLatestValidatorSetRequest,
    GetLatestValidatorSetResponse,
    GetNodeInfoRequest,
    GetNodeInfoResponse,
    GetSyncingRequest,
    GetSyncingResponse,
    GetValidatorSetByHeightRequest,
    GetValidatorSetByHeightResponse,
)
from neurionpy.tendermint.interface import CosmosBaseTendermint


class CosmosBaseTendermintRestClient(CosmosBaseTendermint):
    """Cosmos Base Tendermint REST client."""

    API_URL = "/cosmos/base/tendermint/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def GetNodeInfo(self, request: GetNodeInfoRequest) -> GetNodeInfoResponse:
        """
        GetNodeInfo queries the current node info.

        :param request: GetNodeInfoRequest
        :return: GetNodeInfoResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/node_info",
        )
        return Parse(json_response, GetNodeInfoResponse())

    def GetSyncing(self, request: GetSyncingRequest) -> GetSyncingResponse:
        """
        GetSyncing queries node syncing.

        :param request: GetSyncingRequest
        :return: GetSyncingResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/syncing",
        )
        return Parse(json_response, GetSyncingResponse())

    def GetLatestBlock(self, request: GetLatestBlockRequest) -> GetLatestBlockResponse:
        """
        GetLatestBlock returns the latest block.

        :param request: GetLatestBlockRequest
        :return: GetLatestBlockResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/blocks/latest",
        )
        return Parse(json_response, GetLatestBlockResponse())

    def GetBlockByHeight(
        self, request: GetBlockByHeightRequest
    ) -> GetBlockByHeightResponse:
        """
        GetBlockByHeight queries block for given height.

        :param request: GetBlockByHeightRequest
        :return: GetBlockByHeightResponse
        """
        json_response = self._rest_api.get(f"{self.API_URL}/blocks/{request.height}")
        return Parse(json_response, GetBlockByHeightResponse())

    def GetLatestValidatorSet(
        self, request: GetLatestValidatorSetRequest
    ) -> GetLatestValidatorSetResponse:
        """
        GetLatestValidatorSet queries latest validator-set.

        :param request: GetLatestValidatorSetRequest
        :return: GetLatestValidatorSetResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/validatorsets/latest", request
        )
        return Parse(json_response, GetLatestValidatorSetResponse())

    def GetValidatorSetByHeight(
        self, request: GetValidatorSetByHeightRequest
    ) -> GetValidatorSetByHeightResponse:
        """
        GetValidatorSetByHeight queries validator-set at a given height.

        :param request: GetValidatorSetByHeightRequest
        :return: GetValidatorSetByHeightResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/validatorsets/{request.height}", request
        )
        return Parse(json_response, GetValidatorSetByHeightResponse())
