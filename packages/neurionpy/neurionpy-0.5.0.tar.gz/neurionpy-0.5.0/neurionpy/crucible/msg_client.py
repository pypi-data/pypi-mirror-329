from typing import Optional

from neurionpy.protos.neurion.crucible.tx_pb2 import (
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
    MsgRegisterTrainer,
    MsgRegisterTrainerResponse,
    MsgRegisterScorer,
    MsgRegisterScorerResponse,
    MsgSubmitTrainingResult,
    MsgSubmitTrainingResultResponse,
    MsgStakeToTask,
    MsgStakeToTaskResponse,
    MsgRequestScoringTask,
    MsgRequestScoringTaskResponse,
    MsgSubmitScore,
    MsgSubmitScoreResponse,
    MsgSubmitFinalResult,
    MsgSubmitFinalResultResponse,
    MsgReportModelPlagiarism,
    MsgReportModelPlagiarismResponse,
    MsgAcceptPlagiarismReport,
    MsgAcceptPlagiarismReportResponse,
    MsgRejectPlagiarismReport,
    MsgRejectPlagiarismReportResponse,
    MsgDisputeSubmissionScore,
    MsgDisputeSubmissionScoreResponse,
    MsgStartTask,
    MsgStartTaskResponse,
    MsgAbortTask,
    MsgAbortTaskResponse,
    MsgTriggerTaskToFinalSubmission,
    MsgTriggerTaskToFinalSubmissionResponse,
    MsgTriggerTaskToFinalTesting,
    MsgTriggerTaskToFinalTestingResponse,
    MsgTerminateTask,
    MsgTerminateTaskResponse,
    MsgClaimTaskReward,
    MsgClaimTaskRewardResponse,
    MsgUnstakeFromTask,
    MsgUnstakeFromTaskResponse,
    MsgDisclaimCreatorStatus,
    MsgDisclaimCreatorStatusResponse,
)
from neurionpy.crucible.interface import CrucibleMessage
from neurionpy.synapse.tx import Transaction
from neurionpy.synapse.tx_helpers import SubmittedTx
from neurionpy.synapse.utils import NeurionUtils
from neurionpy.synapse.wallet import Wallet


class CrucibleMsgClient(CrucibleMessage):
    def __init__(self, utils: NeurionUtils, wallet: Optional[Wallet]) -> None:
        """
        Initialize the Crucible message client.

        :param utils: NeurionUtils instance for transaction preparation and broadcasting.
        :param wallet: Wallet instance for signing transactions.
        :raises ValueError: if wallet is not provided.
        """
        if wallet is None:
            raise ValueError("A wallet must be provided to initialize CrucibleMsgClient.")
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

    def RegisterTrainer(
        self,
        message: MsgRegisterTrainer,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Register as a trainer for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RegisterScorer(
        self,
        message: MsgRegisterScorer,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Register as a scorer for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def SubmitTrainingResult(
        self,
        message: MsgSubmitTrainingResult,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Submit a training result for a task."""
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

    def RequestScoringTask(
        self,
        message: MsgRequestScoringTask,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Request scoring for a task."""
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
        """Submit a score for a scoring task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def SubmitFinalResult(
        self,
        message: MsgSubmitFinalResult,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Submit the final result for a task."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def ReportModelPlagiarism(
        self,
        message: MsgReportModelPlagiarism,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Report model plagiarism."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def AcceptPlagiarismReport(
        self,
        message: MsgAcceptPlagiarismReport,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Accept a plagiarism report."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def RejectPlagiarismReport(
        self,
        message: MsgRejectPlagiarismReport,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Reject a plagiarism report."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def DisputeSubmissionScore(
        self,
        message: MsgDisputeSubmissionScore,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Dispute a submission score."""
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

    def TriggerTaskToFinalSubmission(
        self,
        message: MsgTriggerTaskToFinalSubmission,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Trigger task transition to final submission phase."""
        self._set_creator(message)
        tx = Transaction()
        tx.add_message(message)
        return self.utils.prepare_and_broadcast_basic_transaction(
            tx, self.wallet, gas_limit=gas_limit, memo=memo
        )

    def TriggerTaskToFinalTesting(
        self,
        message: MsgTriggerTaskToFinalTesting,
        memo: Optional[str] = None,
        gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Trigger task transition to final testing phase."""
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