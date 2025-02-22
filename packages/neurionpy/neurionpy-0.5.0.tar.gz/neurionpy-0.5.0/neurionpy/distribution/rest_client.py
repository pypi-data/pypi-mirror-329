from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.distribution.interface import Distribution
from neurionpy.protos.cosmos.distribution.v1beta1.query_pb2 import (
    QueryCommunityPoolResponse,
    QueryDelegationRewardsRequest,
    QueryDelegationRewardsResponse,
    QueryDelegationTotalRewardsRequest,
    QueryDelegationTotalRewardsResponse,
    QueryDelegatorValidatorsRequest,
    QueryDelegatorValidatorsResponse,
    QueryDelegatorWithdrawAddressRequest,
    QueryDelegatorWithdrawAddressResponse,
    QueryParamsResponse,
    QueryValidatorCommissionRequest,
    QueryValidatorCommissionResponse,
    QueryValidatorOutstandingRewardsRequest,
    QueryValidatorOutstandingRewardsResponse,
    QueryValidatorSlashesRequest,
    QueryValidatorSlashesResponse,
)


class DistributionRestClient(Distribution):
    """Distribution REST client."""

    API_URL = "/cosmos/distribution/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def CommunityPool(self) -> QueryCommunityPoolResponse:
        """
        CommunityPool queries the community pool coins.

        :return: a QueryCommunityPoolResponse instance
        """
        json_response = self._rest_api.get(f"{self.API_URL}/community_pool")
        return Parse(json_response, QueryCommunityPoolResponse())

    def DelegationTotalRewards(
        self, request: QueryDelegationTotalRewardsRequest
    ) -> QueryDelegationTotalRewardsResponse:
        """
        DelegationTotalRewards queries the total rewards accrued by each validator.

        :param request: a QueryDelegationTotalRewardsRequest instance
        :return: a QueryDelegationTotalRewardsResponse instance
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/delegators/{request.delegator_address}/rewards"
        )
        return Parse(json_response, QueryDelegationTotalRewardsResponse())

    def DelegationRewards(
        self, request: QueryDelegationRewardsRequest
    ) -> QueryDelegationRewardsResponse:
        """
        DelegationRewards queries the total rewards accrued by a delegation.

        :param request: a QueryDelegationRewardsRequest instance
        :return: a QueryDelegationRewardsResponse instance
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/delegators/{request.delegator_address}/rewards/{request.validator_address}"
        )
        return Parse(json_response, QueryDelegationRewardsResponse())

    def DelegatorValidators(
        self, request: QueryDelegatorValidatorsRequest
    ) -> QueryDelegatorValidatorsResponse:
        """
        DelegatorValidators queries the validators of a delegator.

        :param request: a QueryDelegatorValidatorsRequest instance
        :return: a QueryDelegatorValidatorsResponse instance
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/delegators/{request.delegator_address}/validators"
        )
        return Parse(json_response, QueryDelegatorValidatorsResponse())

    def DelegatorWithdrawAddress(
        self, request: QueryDelegatorWithdrawAddressRequest
    ) -> QueryDelegatorWithdrawAddressResponse:
        """
        DelegatorWithdrawAddress queries withdraw address of a delegator.

        :param request: a QueryDelegatorWithdrawAddressRequest instance
        :return: a QueryDelegatorWithdrawAddressResponse instance
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/delegators/{request.delegator_address}/withdraw_address"
        )
        return Parse(json_response, QueryDelegatorWithdrawAddressResponse())

    def Params(self) -> QueryParamsResponse:
        """
        Params queries params of the distribution module.

        :return: a QueryParamsResponse instance
        """
        json_response = self._rest_api.get(f"{self.API_URL}/params")
        return Parse(json_response, QueryParamsResponse())

    def ValidatorCommission(
        self, request: QueryValidatorCommissionRequest
    ) -> QueryValidatorCommissionResponse:
        """
        ValidatorCommission queries accumulated commission for a validator.

        :param request: QueryValidatorCommissionRequest
        :return: QueryValidatorCommissionResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/validators/{request.validator_address}/commission"
        )
        return Parse(json_response, QueryValidatorCommissionResponse())

    def ValidatorOutstandingRewards(
        self, request: QueryValidatorOutstandingRewardsRequest
    ) -> QueryValidatorOutstandingRewardsResponse:
        """
        ValidatorOutstandingRewards queries rewards of a validator address.

        :param request: QueryValidatorOutstandingRewardsRequest
        :return: QueryValidatorOutstandingRewardsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/validators/{request.validator_address}/outstanding_rewards"
        )
        return Parse(json_response, QueryValidatorOutstandingRewardsResponse())

    def ValidatorSlashes(
        self, request: QueryValidatorSlashesRequest
    ) -> QueryValidatorSlashesResponse:
        """
        ValidatorSlashes queries slash events of a validator.

        :param request: QueryValidatorSlashesRequest
        :return: QueryValidatorSlashesResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/validators/{request.validator_address}/slashes",
            request,
            ["validatorAddress"],
        )
        return Parse(json_response, QueryValidatorSlashesResponse())
