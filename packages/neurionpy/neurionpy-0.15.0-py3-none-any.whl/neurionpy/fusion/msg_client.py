from typing import Optional

from neurionpy.protos.neurion.fusion.tx_pb2 import (
    MsgUpdateParams,
    MsgUpdateParamsResponse,
    MsgApplyCreator,
    MsgApplyCreatorResponse,
    MsgApproveApplication,
    MsgApproveApplicationResponse,
    MsgRejectApplication,
    MsgRejectApplicationResponse,
    MsgCreateTask,
    MsgCreateTaskResponse,
    MsgStartTask,
    MsgStartTaskResponse,
    MsgProposeModel,
    MsgProposeModelResponse,
    MsgRegisterProposer,
    MsgRegisterProposerResponse,
    MsgRegisterValidator,
    MsgRegisterValidatorResponse,
    MsgStartTesting,
    MsgStartTestingResponse,
    MsgRequestValidationTask,
    MsgRequestValidationTaskResponse,
    MsgSubmitScore,
    MsgSubmitScoreResponse,
    MsgDisputeModelScore,
    MsgDisputeModelScoreResponse,
    MsgStartNewRound,
    MsgStartNewRoundResponse,
    MsgTerminateTask,
    MsgTerminateTaskResponse,
    MsgStakeToTask,
    MsgStakeToTaskResponse,
    MsgClaimTaskReward,
    MsgClaimTaskRewardResponse,
    MsgUnstakeFromTask,
    MsgUnstakeFromTaskResponse,
    MsgDisclaimCreatorStatus,
    MsgDisclaimCreatorStatusResponse,
    MsgAbortTask,
    MsgAbortTaskResponse,
)
from neurionpy.fusion.interface import FusionMessage
from neurionpy.synapse.tx import Transaction
from neurionpy.synapse.tx_helpers import SubmittedTx
from neurionpy.synapse.utils import NeurionUtils
from neurionpy.synapse.wallet import Wallet


class FusionMsgClient(FusionMessage):
    def __init__(self, utils: NeurionUtils, wallet: Optional[Wallet]) -> None:
        """
        Initialize the Fusion message client.

        :param utils: NeurionUtils instance for transaction preparation and broadcasting.
        :param wallet: Wallet instance for signing transactions.
        :raises ValueError: if wallet is not provided.
        """
        if wallet is None:
            raise ValueError("A wallet must be provided to initialize FusionMsgClient.")
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
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ApplyCreator(
            self,
            message: MsgApplyCreator,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Apply to become a creator."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ApproveApplication(
            self,
            message: MsgApproveApplication,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Approve a creator application."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RejectApplication(
            self,
            message: MsgRejectApplication,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Reject a creator application."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def CreateTask(
            self,
            message: MsgCreateTask,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Create a new task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def StartTask(
            self,
            message: MsgStartTask,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Start a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ProposeModel(
            self,
            message: MsgProposeModel,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Propose a model for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RegisterProposer(
            self,
            message: MsgRegisterProposer,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Register as a proposer for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RegisterValidator(
            self,
            message: MsgRegisterValidator,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Register as a validator for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def StartTesting(
            self,
            message: MsgStartTesting,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Start testing for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RequestValidationTask(
            self,
            message: MsgRequestValidationTask,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Request a validation task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def SubmitScore(
            self,
            message: MsgSubmitScore,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Submit a score for a validation task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def DisputeModelScore(
            self,
            message: MsgDisputeModelScore,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Dispute a model score."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def StartNewRound(
            self,
            message: MsgStartNewRound,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Start a new round for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def TerminateTask(
            self,
            message: MsgTerminateTask,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Terminate a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def StakeToTask(
            self,
            message: MsgStakeToTask,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Stake tokens to a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ClaimTaskReward(
            self,
            message: MsgClaimTaskReward,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Claim reward for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def UnstakeFromTask(
            self,
            message: MsgUnstakeFromTask,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Unstake tokens from a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def DisclaimCreatorStatus(
            self,
            message: MsgDisclaimCreatorStatus,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Disclaim creator status."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def AbortTask(
            self,
            message: MsgAbortTask,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Abort a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )