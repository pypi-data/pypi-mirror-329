from abc import ABC, abstractmethod
from typing import Optional

from neurionpy.protos.neurion.ganglion.query_pb2 import (
    QueryParamsRequest, QueryParamsResponse,
    QueryIonByIonAddressRequest, QueryIonByIonAddressResponse,
    QueryIonByCreatorRequest, QueryIonByCreatorResponse,
    QueryGetValidatorsRequest, QueryGetValidatorsResponse,
    QueryIonsByInputSchemaHashRequest, QueryIonsByInputSchemaHashResponse,
    QueryGetPathwayRequest, QueryGetPathwayResponse,
    QueryListPathwaysRequest, QueryListPathwaysResponse,
    QueryListIonsByAddressesRequest, QueryListIonsByAddressesResponse,
    QueryUserPathwayStakeRequest, QueryUserPathwayStakeResponse,
    QueryGetUserRewardRequest, QueryGetUserRewardResponse,
    QueryGetProtocolFeeRequest, QueryGetProtocolFeeResponse,
    QueryPathwaysUsingIonRequest, QueryPathwaysUsingIonResponse,
    QueryIonsByReportsRequest, QueryIonsByReportsResponse,
    QueryListAllPathwaysRequest, QueryListAllPathwaysResponse,
    QueryGetRewardRequest, QueryGetRewardResponse,
    QueryGetStakeRequest, QueryGetStakeResponse,
    QueryGetIonRequest, QueryGetIonResponse,
    QueryGetPathwayUnstakeInitiatedUsersRequest, QueryGetPathwayUnstakeInitiatedUsersResponse,
    QueryGetStakerRewardRequest, QueryGetStakerRewardResponse,
    QueryGetAvailableIonsRequest, QueryGetAvailableIonsResponse, QueryGetAllowedIpsRequest, QueryGetAllowedIpsResponse
)

from neurionpy.protos.neurion.ganglion.tx_pb2 import (
    MsgUpdateParams, MsgUpdateParamsResponse,
    MsgRegisterIon, MsgRegisterIonResponse,
    MsgReportUnavailableIon, MsgReportUnavailableIonResponse,
    MsgUnreportUnavailableIon, MsgUnreportUnavailableIonResponse,
    MsgAddValidator, MsgAddValidatorResponse,
    MsgRemoveValidator, MsgRemoveValidatorResponse,
    MsgValidateAvailability, MsgValidateAvailabilityResponse,
    MsgRegisterPathway, MsgRegisterPathwayResponse,
    MsgStakePathway, MsgStakePathwayResponse,
    MsgRefundPathwayStake, MsgRefundPathwayStakeResponse,
    MsgInitUnstakePathway, MsgInitUnstakePathwayResponse,
    MsgClaimProtocolFee, MsgClaimProtocolFeeResponse,
    MsgSettlePathwayStake, MsgSettlePathwayStakeResponse,
    MsgStakeToGanglion, MsgStakeToGanglionResponse,
    MsgClaimReward, MsgClaimRewardResponse,
    MsgUnstakeFromGanglion, MsgUnstakeFromGanglionResponse,
    MsgUpdatePathway, MsgUpdatePathwayResponse, MsgRemoveIon, MsgRemovePathway
)

from neurionpy.synapse.tx_helpers import SubmittedTx


class GanglionQuery(ABC):
    """GanglionQuery defines the interface for querying the Ganglion module."""

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """Query the parameters of the Ganglion module."""

    @abstractmethod
    def IonByIonAddress(self, request: QueryIonByIonAddressRequest) -> QueryIonByIonAddressResponse:
        """Query an Ion by its ion_address."""

    @abstractmethod
    def IonByCreator(self, request: QueryIonByCreatorRequest) -> QueryIonByCreatorResponse:
        """Query an Ion by its creator."""

    @abstractmethod
    def GetValidators(self, request: QueryGetValidatorsRequest) -> QueryGetValidatorsResponse:
        """Query the list of validators."""

    @abstractmethod
    def IonsByInputSchemaHash(self, request: QueryIonsByInputSchemaHashRequest) -> QueryIonsByInputSchemaHashResponse:
        """Query Ions by input_schema_hash with pagination."""

    @abstractmethod
    def GetPathway(self, request: QueryGetPathwayRequest) -> QueryGetPathwayResponse:
        """Query a pathway by its ID."""

    @abstractmethod
    def ListPathways(self, request: QueryListPathwaysRequest) -> QueryListPathwaysResponse:
        """List pathways for a creator with pagination."""

    @abstractmethod
    def ListIonsByAddresses(self, request: QueryListIonsByAddressesRequest) -> QueryListIonsByAddressesResponse:
        """List Ions by a list of ion addresses."""

    @abstractmethod
    def UserPathwayStake(self, request: QueryUserPathwayStakeRequest) -> QueryUserPathwayStakeResponse:
        """Query pathway stake for a given pathway and user."""

    @abstractmethod
    def GetUserReward(self, request: QueryGetUserRewardRequest) -> QueryGetUserRewardResponse:
        """Query user reward."""

    @abstractmethod
    def GetProtocolFee(self, request: QueryGetProtocolFeeRequest) -> QueryGetProtocolFeeResponse:
        """Query the protocol fee."""

    @abstractmethod
    def PathwaysUsingIon(self, request: QueryPathwaysUsingIonRequest) -> QueryPathwaysUsingIonResponse:
        """Query pathways using a given ion."""

    @abstractmethod
    def ListAllPathways(self, request: QueryListAllPathwaysRequest) -> QueryListAllPathwaysResponse:
        """List all pathways with pagination."""

    @abstractmethod
    def GetReward(self, request: QueryGetRewardRequest) -> QueryGetRewardResponse:
        """Query reward for a given user."""

    @abstractmethod
    def GetStake(self, request: QueryGetStakeRequest) -> QueryGetStakeResponse:
        """Query stake for a given user."""

    @abstractmethod
    def GetIon(self, request: QueryGetIonRequest) -> QueryGetIonResponse:
        """Query an Ion by its ID."""

    @abstractmethod
    def GetPathwayUnstakeInitiatedUsers(self,
                                        request: QueryGetPathwayUnstakeInitiatedUsersRequest) -> QueryGetPathwayUnstakeInitiatedUsersResponse:
        """Query pathway unstake initiated users."""

    @abstractmethod
    def GetStakerReward(self, request: QueryGetStakerRewardRequest) -> QueryGetStakerRewardResponse:
        """Query staker reward."""

    @abstractmethod
    def GetAvailableIons(self, request: QueryGetAvailableIonsRequest) -> QueryGetAvailableIonsResponse:
        """Query available Ions with pagination."""

    @abstractmethod
    def IonsByReports(self, request: QueryIonsByReportsRequest) -> QueryIonsByReportsResponse:
        """Query ions by reports with pagination."""

    @abstractmethod
    def GetAllowedIps(self, request: QueryGetAllowedIpsRequest) -> QueryGetAllowedIpsResponse:
        """Get allowed IPs."""

class GanglionMessage(ABC):
    """GanglionMessage defines the interface for sending transactions to the Ganglion module."""

    @abstractmethod
    def UpdateParams(self, message: MsgUpdateParams, memo: Optional[str] = None,
                     gas_limit: Optional[int] = None) -> SubmittedTx:
        """Update module parameters."""

    @abstractmethod
    def RegisterIon(self, message: MsgRegisterIon, memo: Optional[str] = None,
                    gas_limit: Optional[int] = None) -> SubmittedTx:
        """Register an Ion."""

    @abstractmethod
    def ReportUnavailableIon(self, message: MsgReportUnavailableIon, memo: Optional[str] = None,
                             gas_limit: Optional[int] = None) -> SubmittedTx:
        """Report an unavailable Ion."""

    @abstractmethod
    def UnreportUnavailableIon(self, message: MsgUnreportUnavailableIon, memo: Optional[str] = None,
                               gas_limit: Optional[int] = None) -> SubmittedTx:
        """Unreport an unavailable Ion."""

    @abstractmethod
    def AddValidator(self, message: MsgAddValidator, memo: Optional[str] = None,
                     gas_limit: Optional[int] = None) -> SubmittedTx:
        """Add a validator."""

    @abstractmethod
    def RemoveValidator(self, message: MsgRemoveValidator, memo: Optional[str] = None,
                        gas_limit: Optional[int] = None) -> SubmittedTx:
        """Remove a validator."""

    @abstractmethod
    def RegisterPathway(self, message: MsgRegisterPathway, memo: Optional[str] = None,
                        gas_limit: Optional[int] = None) -> SubmittedTx:
        """Register a pathway."""

    @abstractmethod
    def StakePathway(self, message: MsgStakePathway, memo: Optional[str] = None,
                     gas_limit: Optional[int] = None) -> SubmittedTx:
        """Stake tokens to a pathway."""

    @abstractmethod
    def RefundPathwayStake(self, message: MsgRefundPathwayStake, memo: Optional[str] = None,
                           gas_limit: Optional[int] = None) -> SubmittedTx:
        """Refund pathway stake."""

    @abstractmethod
    def StakeToGanglion(self, message: MsgStakeToGanglion, memo: Optional[str] = None,
                        gas_limit: Optional[int] = None) -> SubmittedTx:
        """Stake tokens to Ganglion."""

    @abstractmethod
    def ClaimReward(self, message: MsgClaimReward, memo: Optional[str] = None,
                    gas_limit: Optional[int] = None) -> SubmittedTx:
        """Claim reward."""

    @abstractmethod
    def UnstakeFromGanglion(self, message: MsgUnstakeFromGanglion, memo: Optional[str] = None,
                            gas_limit: Optional[int] = None) -> SubmittedTx:
        """Unstake tokens from Ganglion."""

    @abstractmethod
    def UpdatePathway(self, message: MsgUpdatePathway, memo: Optional[str] = None,
                      gas_limit: Optional[int] = None) -> SubmittedTx:
        """Update an existing pathway."""

    @abstractmethod
    def ValidateAvailability(self, message: MsgValidateAvailability, memo: Optional[str] = None,
                             gas_limit: Optional[int] = None) -> SubmittedTx:
        """Validate the availability of an Ion."""

    @abstractmethod
    def InitUnstakePathway(self, message: MsgInitUnstakePathway, memo: Optional[str] = None,
                           gas_limit: Optional[int] = None) -> SubmittedTx:
        """Initiate unstaking for a pathway."""

    @abstractmethod
    def ClaimProtocolFee(self, message: MsgClaimProtocolFee, memo: Optional[str] = None,
                         gas_limit: Optional[int] = None) -> SubmittedTx:
        """Claim the protocol fee."""

    @abstractmethod
    def SettlePathwayStake(self, message: MsgSettlePathwayStake, memo: Optional[str] = None,
                           gas_limit: Optional[int] = None) -> SubmittedTx:
        """Settle a pathway stake."""

    @abstractmethod
    def RemoveIon(self,message: MsgRemoveIon,memo: Optional[str] = None,gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Remove an Ion."""

    @abstractmethod
    def RemovePathway(
            self,
            message: MsgRemovePathway,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Update an existing pathway."""