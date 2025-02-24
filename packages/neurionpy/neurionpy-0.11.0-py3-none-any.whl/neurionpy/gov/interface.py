from abc import ABC, abstractmethod

from neurionpy.protos.cosmos.gov.v1beta1.query_pb2 import (
    QueryDepositRequest,
    QueryDepositResponse,
    QueryDepositsRequest,
    QueryDepositsResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QueryProposalRequest,
    QueryProposalResponse,
    QueryProposalsRequest,
    QueryProposalsResponse,
    QueryTallyResultRequest,
    QueryTallyResultResponse,
    QueryVoteRequest,
    QueryVoteResponse,
    QueryVotesRequest,
    QueryVotesResponse,
)


class Gov(ABC):
    """Gov abstract class."""

    @abstractmethod
    def Proposal(self, request: QueryProposalRequest) -> QueryProposalResponse:
        """
        Proposal queries proposal details based on ProposalID.

        :param request: QueryProposalRequest with proposal id

        :return: QueryProposalResponse
        """

    @abstractmethod
    def Proposals(self, request: QueryProposalsRequest) -> QueryProposalsResponse:
        """
        Proposals queries all proposals based on given status.

        :param request: QueryProposalsRequest

        :return: QueryProposalsResponse
        """

    @abstractmethod
    def Vote(self, request: QueryVoteRequest) -> QueryVoteResponse:
        """
        Vote queries voted information based on proposalID, voterAddr.

        :param request: QueryVoteRequest with voter and proposal id

        :return: QueryVoteResponse
        """

    @abstractmethod
    def Votes(self, request: QueryVotesRequest) -> QueryVotesResponse:
        """
        Votes queries votes of a given proposal.

        :param request: QueryVotesResponse with proposal id

        :return: QueryVotesResponse
        """

    @abstractmethod
    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Params queries all parameters of the gov module.

        :param request: QueryParamsRequest with params_type

        :return: QueryParamsResponse
        """

    @abstractmethod
    def Deposit(self, request: QueryDepositRequest) -> QueryDepositResponse:
        """
        Deposit queries single deposit information based proposalID, depositAddr.

        :param request: QueryDepositRequest with depositor and proposal_id

        :return: QueryDepositResponse
        """

    @abstractmethod
    def Deposits(self, request: QueryDepositsRequest) -> QueryDepositsResponse:
        """Deposits queries all deposits of a single proposal.

        :param request: QueryDepositsRequest with proposal_id

        :return: QueryDepositsResponse
        """

    @abstractmethod
    def TallyResult(self, request: QueryTallyResultRequest) -> QueryTallyResultResponse:
        """
        Tally Result queries the tally of a proposal vote.

        :param request: QueryTallyResultRequest with proposal_id

        :return: QueryTallyResultResponse
        """
