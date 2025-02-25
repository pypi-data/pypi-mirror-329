from typing import Optional

from neurionpy.protos.neurion.ganglion.tx_pb2 import (
    MsgUpdateParams,
    MsgUpdateParamsResponse,
    MsgRegisterIon,
    MsgRegisterIonResponse,
    MsgReportUnavailableIon,
    MsgReportUnavailableIonResponse,
    MsgUnreportUnavailableIon,
    MsgUnreportUnavailableIonResponse,
    MsgAddValidator,
    MsgAddValidatorResponse,
    MsgRemoveValidator,
    MsgRemoveValidatorResponse,
    MsgValidateAvailability,
    MsgValidateAvailabilityResponse,
    MsgRegisterPathway,
    MsgRegisterPathwayResponse,
    MsgStakePathway,
    MsgStakePathwayResponse,
    MsgRefundPathwayStake,
    MsgRefundPathwayStakeResponse,
    MsgInitUnstakePathway,
    MsgInitUnstakePathwayResponse,
    MsgClaimProtocolFee,
    MsgClaimProtocolFeeResponse,
    MsgSettlePathwayStake,
    MsgSettlePathwayStakeResponse,
    MsgStakeToGanglion,
    MsgStakeToGanglionResponse,
    MsgClaimReward,
    MsgClaimRewardResponse,
    MsgUnstakeFromGanglion,
    MsgUnstakeFromGanglionResponse,
    MsgUpdatePathway,
    MsgUpdatePathwayResponse, MsgRemoveIon, MsgRemovePathway,
)
from neurionpy.ganglion.interface import GanglionMessage
from neurionpy.synapse.tx import Transaction
from neurionpy.synapse.tx_helpers import SubmittedTx
from neurionpy.synapse.utils import NeurionUtils
from neurionpy.synapse.wallet import Wallet


class GanglionMsgClient(GanglionMessage):
    def __init__(self, utils: NeurionUtils, wallet: Optional[Wallet]) -> None:
        """
        Initialize the Ganglion message client.

        :param utils: NeurionUtils instance for transaction preparation and broadcasting.
        :param wallet: Wallet instance for signing transactions.
        """
        if wallet is None:
            raise ValueError("A wallet must be provided to initialize GanglionMsgClient.")
        self.utils = utils
        self.wallet = wallet

    def _set_creator(self, message):
        """
        If the message has a 'creator' field and it is not set, assign the wallet address.
        """
        if hasattr(message, "creator") and not message.creator:
            message.creator = str(self.wallet.address())

    def UpdateParams(
        self,
        message: MsgUpdateParams,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Update module parameters.
        Note: This message uses an 'authority' field, so no creator defaulting.
        """
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RegisterIon(
        self,
        message: MsgRegisterIon,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Register an Ion."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RemoveIon(
        self,
        message: MsgRemoveIon,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Update an existing pathway."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ReportUnavailableIon(
        self,
        message: MsgReportUnavailableIon,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Report an unavailable Ion."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def UnreportUnavailableIon(
        self,
        message: MsgUnreportUnavailableIon,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Unreport an unavailable Ion."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def AddValidator(
        self,
        message: MsgAddValidator,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Add a validator."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RemoveValidator(
        self,
        message: MsgRemoveValidator,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Remove a validator."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ValidateAvailability(
        self,
        message: MsgValidateAvailability,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Validate the availability of an Ion."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RegisterPathway(
        self,
        message: MsgRegisterPathway,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Register a pathway."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def StakePathway(
        self,
        message: MsgStakePathway,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Stake tokens to a pathway."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RefundPathwayStake(
        self,
        message: MsgRefundPathwayStake,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Refund pathway stake."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def InitUnstakePathway(
        self,
        message: MsgInitUnstakePathway,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Initiate unstaking for a pathway."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ClaimProtocolFee(
        self,
        message: MsgClaimProtocolFee,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Claim the protocol fee."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def SettlePathwayStake(
        self,
        message: MsgSettlePathwayStake,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Settle a pathway stake."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def StakeToGanglion(
        self,
        message: MsgStakeToGanglion,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Stake tokens to Ganglion."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ClaimReward(
        self,
        message: MsgClaimReward,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Claim reward."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def UnstakeFromGanglion(
        self,
        message: MsgUnstakeFromGanglion,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Unstake tokens from Ganglion."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def UpdatePathway(
        self,
        message: MsgUpdatePathway,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Update an existing pathway."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RemovePathway(
        self,
        message: MsgRemovePathway,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Update an existing pathway."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )