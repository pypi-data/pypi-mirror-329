from neurionpy.protos.neurion.sanctum.tx_pb2 import (
    MsgSubmitDatasetApplication, MsgSubmitDatasetApplicationResponse,
    MsgApproveApplication, MsgApproveApplicationResponse,
    MsgRejectApplication, MsgRejectApplicationResponse,
    MsgDisclaimDataset, MsgDisclaimDatasetResponse,
    MsgRequestToUseDataset, MsgRequestToUseDatasetResponse,
    MsgCancelDatasetUsageRequest, MsgCancelDatasetUsageRequestResponse,
    MsgRejectDatasetUsageRequest, MsgRejectDatasetUsageRequestResponse,
    MsgApproveDatasetUsageRequest, MsgApproveDatasetUsageRequestResponse,
    MsgAddProcessor, MsgAddProcessorResponse,
    MsgRemoveProcessor, MsgRemoveProcessorResponse,
    MsgProcessDatasetUsageRequest, MsgProcessDatasetUsageRequestResponse,
    MsgFinishDatasetUsageRequest, MsgFinishDatasetUsageRequestResponse,
    MsgDisputeDatasetUsageRequest, MsgDisputeDatasetUsageRequestResponse,
    MsgApproveDispute, MsgApproveDisputeResponse,
    MsgRejectDispute, MsgRejectDisputeResponse,
    MsgStakeToSanctum, MsgStakeToSanctumResponse,
    MsgUnstakeFromSanctum, MsgUnstakeFromSanctumResponse,
    MsgClaimReward, MsgClaimRewardResponse,
)

from neurionpy.synapse.tx_helpers import SubmittedTx

from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.sanctum.query_pb2 import (
    QueryParamsRequest, QueryParamsResponse,
    QueryGetAvailableDatasetsRequest, QueryGetAvailableDatasetsResponse,
    QueryGetApprovedUsageRequestsRequest, QueryGetApprovedUsageRequestsResponse,
    QueryGetRewardRequest, QueryGetRewardResponse,
    QueryGetStakeRequest, QueryGetStakeResponse,
    QueryGetPendingDatasetsRequest, QueryGetPendingDatasetsResponse,
    QueryGetPendingUsageRequestsRequest, QueryGetPendingUsageRequestsResponse,
    QueryGetDatasetRequest, QueryGetDatasetResponse,
    QueryGetUsageRequestRequest, QueryGetUsageRequestResponse,
    QueryGetUsageRequestsForDatasetRequest, QueryGetUsageRequestsForDatasetResponse,
    QueryGetUsageRequestsForUserRequest, QueryGetUsageRequestsForUserResponse,
    QueryGetDatasetsForUserRequest, QueryGetDatasetsForUserResponse,
)


class SanctumQuery(ABC):
    """Sanctum abstract class defining query methods."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Query module parameters."""

    @abstractmethod
    def GetAvailableDatasets(self, request: QueryGetAvailableDatasetsRequest) -> QueryGetAvailableDatasetsResponse:
        """Query available datasets with pagination."""

    @abstractmethod
    def GetApprovedUsageRequests(self, request: QueryGetApprovedUsageRequestsRequest) -> QueryGetApprovedUsageRequestsResponse:
        """Query approved dataset usage requests."""

    @abstractmethod
    def GetReward(self, request: QueryGetRewardRequest) -> QueryGetRewardResponse:
        """Query the reward for a user."""

    @abstractmethod
    def GetStake(self, request: QueryGetStakeRequest) -> QueryGetStakeResponse:
        """Query the stake for a user."""

    @abstractmethod
    def GetPendingDatasets(self, request: QueryGetPendingDatasetsRequest) -> QueryGetPendingDatasetsResponse:
        """Query pending dataset applications."""

    @abstractmethod
    def GetPendingUsageRequests(self, request: QueryGetPendingUsageRequestsRequest) -> QueryGetPendingUsageRequestsResponse:
        """Query pending usage requests for a user."""

    @abstractmethod
    def GetDataset(self, request: QueryGetDatasetRequest) -> QueryGetDatasetResponse:
        """Query details of a specific dataset."""

    @abstractmethod
    def GetUsageRequest(self, request: QueryGetUsageRequestRequest) -> QueryGetUsageRequestResponse:
        """Query details of a specific dataset usage request."""

    @abstractmethod
    def GetUsageRequestsForDataset(self, request: QueryGetUsageRequestsForDatasetRequest) -> QueryGetUsageRequestsForDatasetResponse:
        """Query usage requests for a specific dataset with pagination."""

    @abstractmethod
    def GetUsageRequestsForUser(self, request: QueryGetUsageRequestsForUserRequest) -> QueryGetUsageRequestsForUserResponse:
        """Query usage requests made by a user with pagination."""

    @abstractmethod
    def GetDatasetsForUser(self, request: QueryGetDatasetsForUserRequest) -> QueryGetDatasetsForUserResponse:
        """Query datasets owned by a user with pagination."""


class SanctumMessage(ABC):
    """Sanctum abstract class defining message methods."""

    @abstractmethod
    def SubmitDatasetApplication(self, message: MsgSubmitDatasetApplication,
                                 memo: Optional[str] = None,
                                 gas_limit: Optional[int] = None) -> SubmittedTx:
        """Submit a dataset application."""

    @abstractmethod
    def ApproveApplication(self, message: MsgApproveApplication,
                           memo: Optional[str] = None,
                           gas_limit: Optional[int] = None) -> SubmittedTx:
        """Approve a dataset application."""

    @abstractmethod
    def RejectApplication(self, message: MsgRejectApplication,
                          memo: Optional[str] = None,
                          gas_limit: Optional[int] = None) -> SubmittedTx:
        """Reject a dataset application."""

    @abstractmethod
    def DisclaimDataset(self, message: MsgDisclaimDataset,
                        memo: Optional[str] = None,
                        gas_limit: Optional[int] = None) -> SubmittedTx:
        """Disclaim a dataset."""

    @abstractmethod
    def RequestToUseDataset(self, message: MsgRequestToUseDataset,
                            memo: Optional[str] = None,
                            gas_limit: Optional[int] = None) -> SubmittedTx:
        """Request to use a dataset."""

    @abstractmethod
    def CancelDatasetUsageRequest(self, message: MsgCancelDatasetUsageRequest,
                                  memo: Optional[str] = None,
                                  gas_limit: Optional[int] = None) -> SubmittedTx:
        """Cancel a dataset usage request."""

    @abstractmethod
    def RejectDatasetUsageRequest(self, message: MsgRejectDatasetUsageRequest,
                                  memo: Optional[str] = None,
                                  gas_limit: Optional[int] = None) -> SubmittedTx:
        """Reject a dataset usage request."""

    @abstractmethod
    def ApproveDatasetUsageRequest(self, message: MsgApproveDatasetUsageRequest,
                                   memo: Optional[str] = None,
                                   gas_limit: Optional[int] = None) -> SubmittedTx:
        """Approve a dataset usage request."""

    @abstractmethod
    def AddProcessor(self, message: MsgAddProcessor,
                     memo: Optional[str] = None,
                     gas_limit: Optional[int] = None) -> SubmittedTx:
        """Add a processor."""

    @abstractmethod
    def RemoveProcessor(self, message: MsgRemoveProcessor,
                        memo: Optional[str] = None,
                        gas_limit: Optional[int] = None) -> SubmittedTx:
        """Remove a processor."""

    @abstractmethod
    def ProcessDatasetUsageRequest(self, message: MsgProcessDatasetUsageRequest,
                                   memo: Optional[str] = None,
                                   gas_limit: Optional[int] = None) -> SubmittedTx:
        """Process a dataset usage request."""

    @abstractmethod
    def FinishDatasetUsageRequest(self, message: MsgFinishDatasetUsageRequest,
                                  memo: Optional[str] = None,
                                  gas_limit: Optional[int] = None) -> SubmittedTx:
        """Finish a dataset usage request."""

    @abstractmethod
    def DisputeDatasetUsageRequest(self, message: MsgDisputeDatasetUsageRequest,
                                   memo: Optional[str] = None,
                                   gas_limit: Optional[int] = None) -> SubmittedTx:
        """Dispute a dataset usage request."""

    @abstractmethod
    def ApproveDispute(self, message: MsgApproveDispute,
                       memo: Optional[str] = None,
                       gas_limit: Optional[int] = None) -> SubmittedTx:
        """Approve a dispute."""

    @abstractmethod
    def RejectDispute(self, message: MsgRejectDispute,
                      memo: Optional[str] = None,
                      gas_limit: Optional[int] = None) -> SubmittedTx:
        """Reject a dispute."""

    @abstractmethod
    def StakeToSanctum(self, message: MsgStakeToSanctum,
                       memo: Optional[str] = None,
                       gas_limit: Optional[int] = None) -> SubmittedTx:
        """Stake tokens to Sanctum."""

    @abstractmethod
    def UnstakeFromSanctum(self, message: MsgUnstakeFromSanctum,
                           memo: Optional[str] = None,
                           gas_limit: Optional[int] = None) -> SubmittedTx:
        """Unstake tokens from Sanctum."""

    @abstractmethod
    def ClaimReward(self, message: MsgClaimReward,
                    memo: Optional[str] = None,
                    gas_limit: Optional[int] = None) -> SubmittedTx:
        """Claim reward."""