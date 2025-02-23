from typing import Optional

from neurionpy.protos.neurion.sanctum.tx_pb2 import (
    MsgUpdateParams,
    MsgUpdateParamsResponse,
    MsgSubmitDatasetApplication,
    MsgSubmitDatasetApplicationResponse,
    MsgApproveApplication,
    MsgApproveApplicationResponse,
    MsgRejectApplication,
    MsgRejectApplicationResponse,
    MsgDisclaimDataset,
    MsgDisclaimDatasetResponse,
    MsgRequestToUseDataset,
    MsgRequestToUseDatasetResponse,
    MsgCancelDatasetUsageRequest,
    MsgCancelDatasetUsageRequestResponse,
    MsgRejectDatasetUsageRequest,
    MsgRejectDatasetUsageRequestResponse,
    MsgApproveDatasetUsageRequest,
    MsgApproveDatasetUsageRequestResponse,
    MsgAddProcessor,
    MsgAddProcessorResponse,
    MsgRemoveProcessor,
    MsgRemoveProcessorResponse,
    MsgProcessDatasetUsageRequest,
    MsgProcessDatasetUsageRequestResponse,
    MsgFinishDatasetUsageRequest,
    MsgFinishDatasetUsageRequestResponse,
    MsgDisputeDatasetUsageRequest,
    MsgDisputeDatasetUsageRequestResponse,
    MsgApproveDispute,
    MsgApproveDisputeResponse,
    MsgRejectDispute,
    MsgRejectDisputeResponse,
    MsgStakeToSanctum,
    MsgStakeToSanctumResponse,
    MsgUnstakeFromSanctum,
    MsgUnstakeFromSanctumResponse,
    MsgClaimReward,
    MsgClaimRewardResponse,
)
from neurionpy.sanctum.interface import SanctumMessage
from neurionpy.synapse.tx import Transaction
from neurionpy.synapse.tx_helpers import SubmittedTx
from neurionpy.synapse.utils import NeurionUtils
from neurionpy.synapse.wallet import Wallet


class SanctumMsgClient(SanctumMessage):
    def __init__(self, utils: NeurionUtils, wallet: Optional[Wallet]) -> None:
        """
        Initialize the Sanctum message client.

        :param utils: NeurionUtils instance for transaction preparation and broadcasting.
        :param wallet: Wallet instance for signing transactions.
        :raises ValueError: if wallet is not provided.
        """
        if wallet is None:
            raise ValueError("A wallet must be provided to initialize SanctumMsgClient.")
        self.utils = utils
        self.wallet = wallet

    def _set_creator(self, message) -> None:
        """
        If the message has a 'creator' field and it is not set, assign it to the wallet's address.
        """
        if hasattr(message, "creator") and not bool(message.creator):
            message.creator = str(self.wallet.address())

    def UpdateParams(
            self,
            message: MsgUpdateParams,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Update module parameters.

        Note: This message uses an 'authority' field, so no creator defaulting is applied.
        """
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def SubmitDatasetApplication(
            self,
            message: MsgSubmitDatasetApplication,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Submit a dataset application.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def ApproveApplication(
            self,
            message: MsgApproveApplication,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Approve a dataset application.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def RejectApplication(
            self,
            message: MsgRejectApplication,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Reject a dataset application.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def DisclaimDataset(
            self,
            message: MsgDisclaimDataset,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Disclaim a dataset.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def RequestToUseDataset(
            self,
            message: MsgRequestToUseDataset,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Request to use a dataset.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def CancelDatasetUsageRequest(
            self,
            message: MsgCancelDatasetUsageRequest,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Cancel a dataset usage request.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def RejectDatasetUsageRequest(
            self,
            message: MsgRejectDatasetUsageRequest,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Reject a dataset usage request.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def ApproveDatasetUsageRequest(
            self,
            message: MsgApproveDatasetUsageRequest,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Approve a dataset usage request.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def AddProcessor(
            self,
            message: MsgAddProcessor,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Add a processor.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def RemoveProcessor(
            self,
            message: MsgRemoveProcessor,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Remove a processor.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def ProcessDatasetUsageRequest(
            self,
            message: MsgProcessDatasetUsageRequest,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Process a dataset usage request.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def FinishDatasetUsageRequest(
            self,
            message: MsgFinishDatasetUsageRequest,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Finish a dataset usage request.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def DisputeDatasetUsageRequest(
            self,
            message: MsgDisputeDatasetUsageRequest,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Dispute a dataset usage request.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def ApproveDispute(
            self,
            message: MsgApproveDispute,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Approve a dispute.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def RejectDispute(
            self,
            message: MsgRejectDispute,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Reject a dispute.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def StakeToSanctum(
            self,
            message: MsgStakeToSanctum,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Stake tokens to Sanctum.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def UnstakeFromSanctum(
            self,
            message: MsgUnstakeFromSanctum,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Unstake tokens from Sanctum.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)

    def ClaimReward(
            self,
            message: MsgClaimReward,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """
        Claim reward.
        """
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(tx, self.wallet, gas_limit=gas_limit, memo=memo)