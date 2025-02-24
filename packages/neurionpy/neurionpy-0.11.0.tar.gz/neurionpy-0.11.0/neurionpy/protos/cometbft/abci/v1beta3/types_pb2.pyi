from cometbft.abci.v1beta1 import types_pb2 as _types_pb2
from cometbft.abci.v1beta2 import types_pb2 as _types_pb2_1
from cometbft.types.v1 import params_pb2 as _params_pb2
from cometbft.types.v1beta1 import validator_pb2 as _validator_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ("echo", "flush", "info", "init_chain", "query", "check_tx", "commit", "list_snapshots", "offer_snapshot", "load_snapshot_chunk", "apply_snapshot_chunk", "prepare_proposal", "process_proposal", "extend_vote", "verify_vote_extension", "finalize_block")
    ECHO_FIELD_NUMBER: _ClassVar[int]
    FLUSH_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    INIT_CHAIN_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    CHECK_TX_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    LIST_SNAPSHOTS_FIELD_NUMBER: _ClassVar[int]
    OFFER_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    LOAD_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    APPLY_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    PREPARE_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    PROCESS_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    EXTEND_VOTE_FIELD_NUMBER: _ClassVar[int]
    VERIFY_VOTE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FINALIZE_BLOCK_FIELD_NUMBER: _ClassVar[int]
    echo: _types_pb2.RequestEcho
    flush: _types_pb2.RequestFlush
    info: _types_pb2_1.RequestInfo
    init_chain: RequestInitChain
    query: _types_pb2.RequestQuery
    check_tx: _types_pb2.RequestCheckTx
    commit: _types_pb2.RequestCommit
    list_snapshots: _types_pb2.RequestListSnapshots
    offer_snapshot: _types_pb2.RequestOfferSnapshot
    load_snapshot_chunk: _types_pb2.RequestLoadSnapshotChunk
    apply_snapshot_chunk: _types_pb2.RequestApplySnapshotChunk
    prepare_proposal: RequestPrepareProposal
    process_proposal: RequestProcessProposal
    extend_vote: RequestExtendVote
    verify_vote_extension: RequestVerifyVoteExtension
    finalize_block: RequestFinalizeBlock
    def __init__(self, echo: _Optional[_Union[_types_pb2.RequestEcho, _Mapping]] = ..., flush: _Optional[_Union[_types_pb2.RequestFlush, _Mapping]] = ..., info: _Optional[_Union[_types_pb2_1.RequestInfo, _Mapping]] = ..., init_chain: _Optional[_Union[RequestInitChain, _Mapping]] = ..., query: _Optional[_Union[_types_pb2.RequestQuery, _Mapping]] = ..., check_tx: _Optional[_Union[_types_pb2.RequestCheckTx, _Mapping]] = ..., commit: _Optional[_Union[_types_pb2.RequestCommit, _Mapping]] = ..., list_snapshots: _Optional[_Union[_types_pb2.RequestListSnapshots, _Mapping]] = ..., offer_snapshot: _Optional[_Union[_types_pb2.RequestOfferSnapshot, _Mapping]] = ..., load_snapshot_chunk: _Optional[_Union[_types_pb2.RequestLoadSnapshotChunk, _Mapping]] = ..., apply_snapshot_chunk: _Optional[_Union[_types_pb2.RequestApplySnapshotChunk, _Mapping]] = ..., prepare_proposal: _Optional[_Union[RequestPrepareProposal, _Mapping]] = ..., process_proposal: _Optional[_Union[RequestProcessProposal, _Mapping]] = ..., extend_vote: _Optional[_Union[RequestExtendVote, _Mapping]] = ..., verify_vote_extension: _Optional[_Union[RequestVerifyVoteExtension, _Mapping]] = ..., finalize_block: _Optional[_Union[RequestFinalizeBlock, _Mapping]] = ...) -> None: ...

class RequestInitChain(_message.Message):
    __slots__ = ("time", "chain_id", "consensus_params", "validators", "app_state_bytes", "initial_height")
    TIME_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_PARAMS_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    APP_STATE_BYTES_FIELD_NUMBER: _ClassVar[int]
    INITIAL_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    time: _timestamp_pb2.Timestamp
    chain_id: str
    consensus_params: _params_pb2.ConsensusParams
    validators: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    app_state_bytes: bytes
    initial_height: int
    def __init__(self, time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., chain_id: _Optional[str] = ..., consensus_params: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]] = ..., validators: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]] = ..., app_state_bytes: _Optional[bytes] = ..., initial_height: _Optional[int] = ...) -> None: ...

class RequestPrepareProposal(_message.Message):
    __slots__ = ("max_tx_bytes", "txs", "local_last_commit", "misbehavior", "height", "time", "next_validators_hash", "proposer_address")
    MAX_TX_BYTES_FIELD_NUMBER: _ClassVar[int]
    TXS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_LAST_COMMIT_FIELD_NUMBER: _ClassVar[int]
    MISBEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    NEXT_VALIDATORS_HASH_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    max_tx_bytes: int
    txs: _containers.RepeatedScalarFieldContainer[bytes]
    local_last_commit: ExtendedCommitInfo
    misbehavior: _containers.RepeatedCompositeFieldContainer[_types_pb2_1.Misbehavior]
    height: int
    time: _timestamp_pb2.Timestamp
    next_validators_hash: bytes
    proposer_address: bytes
    def __init__(self, max_tx_bytes: _Optional[int] = ..., txs: _Optional[_Iterable[bytes]] = ..., local_last_commit: _Optional[_Union[ExtendedCommitInfo, _Mapping]] = ..., misbehavior: _Optional[_Iterable[_Union[_types_pb2_1.Misbehavior, _Mapping]]] = ..., height: _Optional[int] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., next_validators_hash: _Optional[bytes] = ..., proposer_address: _Optional[bytes] = ...) -> None: ...

class RequestProcessProposal(_message.Message):
    __slots__ = ("txs", "proposed_last_commit", "misbehavior", "hash", "height", "time", "next_validators_hash", "proposer_address")
    TXS_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_LAST_COMMIT_FIELD_NUMBER: _ClassVar[int]
    MISBEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    NEXT_VALIDATORS_HASH_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    txs: _containers.RepeatedScalarFieldContainer[bytes]
    proposed_last_commit: CommitInfo
    misbehavior: _containers.RepeatedCompositeFieldContainer[_types_pb2_1.Misbehavior]
    hash: bytes
    height: int
    time: _timestamp_pb2.Timestamp
    next_validators_hash: bytes
    proposer_address: bytes
    def __init__(self, txs: _Optional[_Iterable[bytes]] = ..., proposed_last_commit: _Optional[_Union[CommitInfo, _Mapping]] = ..., misbehavior: _Optional[_Iterable[_Union[_types_pb2_1.Misbehavior, _Mapping]]] = ..., hash: _Optional[bytes] = ..., height: _Optional[int] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., next_validators_hash: _Optional[bytes] = ..., proposer_address: _Optional[bytes] = ...) -> None: ...

class RequestExtendVote(_message.Message):
    __slots__ = ("hash", "height", "time", "txs", "proposed_last_commit", "misbehavior", "next_validators_hash", "proposer_address")
    HASH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TXS_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_LAST_COMMIT_FIELD_NUMBER: _ClassVar[int]
    MISBEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    NEXT_VALIDATORS_HASH_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    height: int
    time: _timestamp_pb2.Timestamp
    txs: _containers.RepeatedScalarFieldContainer[bytes]
    proposed_last_commit: CommitInfo
    misbehavior: _containers.RepeatedCompositeFieldContainer[_types_pb2_1.Misbehavior]
    next_validators_hash: bytes
    proposer_address: bytes
    def __init__(self, hash: _Optional[bytes] = ..., height: _Optional[int] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., txs: _Optional[_Iterable[bytes]] = ..., proposed_last_commit: _Optional[_Union[CommitInfo, _Mapping]] = ..., misbehavior: _Optional[_Iterable[_Union[_types_pb2_1.Misbehavior, _Mapping]]] = ..., next_validators_hash: _Optional[bytes] = ..., proposer_address: _Optional[bytes] = ...) -> None: ...

class RequestVerifyVoteExtension(_message.Message):
    __slots__ = ("hash", "validator_address", "height", "vote_extension")
    HASH_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    VOTE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    validator_address: bytes
    height: int
    vote_extension: bytes
    def __init__(self, hash: _Optional[bytes] = ..., validator_address: _Optional[bytes] = ..., height: _Optional[int] = ..., vote_extension: _Optional[bytes] = ...) -> None: ...

class RequestFinalizeBlock(_message.Message):
    __slots__ = ("txs", "decided_last_commit", "misbehavior", "hash", "height", "time", "next_validators_hash", "proposer_address")
    TXS_FIELD_NUMBER: _ClassVar[int]
    DECIDED_LAST_COMMIT_FIELD_NUMBER: _ClassVar[int]
    MISBEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    NEXT_VALIDATORS_HASH_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    txs: _containers.RepeatedScalarFieldContainer[bytes]
    decided_last_commit: CommitInfo
    misbehavior: _containers.RepeatedCompositeFieldContainer[_types_pb2_1.Misbehavior]
    hash: bytes
    height: int
    time: _timestamp_pb2.Timestamp
    next_validators_hash: bytes
    proposer_address: bytes
    def __init__(self, txs: _Optional[_Iterable[bytes]] = ..., decided_last_commit: _Optional[_Union[CommitInfo, _Mapping]] = ..., misbehavior: _Optional[_Iterable[_Union[_types_pb2_1.Misbehavior, _Mapping]]] = ..., hash: _Optional[bytes] = ..., height: _Optional[int] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., next_validators_hash: _Optional[bytes] = ..., proposer_address: _Optional[bytes] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("exception", "echo", "flush", "info", "init_chain", "query", "check_tx", "commit", "list_snapshots", "offer_snapshot", "load_snapshot_chunk", "apply_snapshot_chunk", "prepare_proposal", "process_proposal", "extend_vote", "verify_vote_extension", "finalize_block")
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    FLUSH_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    INIT_CHAIN_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    CHECK_TX_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    LIST_SNAPSHOTS_FIELD_NUMBER: _ClassVar[int]
    OFFER_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    LOAD_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    APPLY_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    PREPARE_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    PROCESS_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    EXTEND_VOTE_FIELD_NUMBER: _ClassVar[int]
    VERIFY_VOTE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FINALIZE_BLOCK_FIELD_NUMBER: _ClassVar[int]
    exception: _types_pb2.ResponseException
    echo: _types_pb2.ResponseEcho
    flush: _types_pb2.ResponseFlush
    info: _types_pb2.ResponseInfo
    init_chain: ResponseInitChain
    query: _types_pb2.ResponseQuery
    check_tx: ResponseCheckTx
    commit: ResponseCommit
    list_snapshots: _types_pb2.ResponseListSnapshots
    offer_snapshot: _types_pb2.ResponseOfferSnapshot
    load_snapshot_chunk: _types_pb2.ResponseLoadSnapshotChunk
    apply_snapshot_chunk: _types_pb2.ResponseApplySnapshotChunk
    prepare_proposal: _types_pb2_1.ResponsePrepareProposal
    process_proposal: _types_pb2_1.ResponseProcessProposal
    extend_vote: ResponseExtendVote
    verify_vote_extension: ResponseVerifyVoteExtension
    finalize_block: ResponseFinalizeBlock
    def __init__(self, exception: _Optional[_Union[_types_pb2.ResponseException, _Mapping]] = ..., echo: _Optional[_Union[_types_pb2.ResponseEcho, _Mapping]] = ..., flush: _Optional[_Union[_types_pb2.ResponseFlush, _Mapping]] = ..., info: _Optional[_Union[_types_pb2.ResponseInfo, _Mapping]] = ..., init_chain: _Optional[_Union[ResponseInitChain, _Mapping]] = ..., query: _Optional[_Union[_types_pb2.ResponseQuery, _Mapping]] = ..., check_tx: _Optional[_Union[ResponseCheckTx, _Mapping]] = ..., commit: _Optional[_Union[ResponseCommit, _Mapping]] = ..., list_snapshots: _Optional[_Union[_types_pb2.ResponseListSnapshots, _Mapping]] = ..., offer_snapshot: _Optional[_Union[_types_pb2.ResponseOfferSnapshot, _Mapping]] = ..., load_snapshot_chunk: _Optional[_Union[_types_pb2.ResponseLoadSnapshotChunk, _Mapping]] = ..., apply_snapshot_chunk: _Optional[_Union[_types_pb2.ResponseApplySnapshotChunk, _Mapping]] = ..., prepare_proposal: _Optional[_Union[_types_pb2_1.ResponsePrepareProposal, _Mapping]] = ..., process_proposal: _Optional[_Union[_types_pb2_1.ResponseProcessProposal, _Mapping]] = ..., extend_vote: _Optional[_Union[ResponseExtendVote, _Mapping]] = ..., verify_vote_extension: _Optional[_Union[ResponseVerifyVoteExtension, _Mapping]] = ..., finalize_block: _Optional[_Union[ResponseFinalizeBlock, _Mapping]] = ...) -> None: ...

class ResponseInitChain(_message.Message):
    __slots__ = ("consensus_params", "validators", "app_hash")
    CONSENSUS_PARAMS_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    APP_HASH_FIELD_NUMBER: _ClassVar[int]
    consensus_params: _params_pb2.ConsensusParams
    validators: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    app_hash: bytes
    def __init__(self, consensus_params: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]] = ..., validators: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]] = ..., app_hash: _Optional[bytes] = ...) -> None: ...

class ResponseCheckTx(_message.Message):
    __slots__ = ("code", "data", "log", "info", "gas_wanted", "gas_used", "events", "codespace")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    GAS_WANTED_FIELD_NUMBER: _ClassVar[int]
    GAS_USED_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    CODESPACE_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: bytes
    log: str
    info: str
    gas_wanted: int
    gas_used: int
    events: _containers.RepeatedCompositeFieldContainer[_types_pb2_1.Event]
    codespace: str
    def __init__(self, code: _Optional[int] = ..., data: _Optional[bytes] = ..., log: _Optional[str] = ..., info: _Optional[str] = ..., gas_wanted: _Optional[int] = ..., gas_used: _Optional[int] = ..., events: _Optional[_Iterable[_Union[_types_pb2_1.Event, _Mapping]]] = ..., codespace: _Optional[str] = ...) -> None: ...

class ResponseCommit(_message.Message):
    __slots__ = ("retain_height",)
    RETAIN_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    retain_height: int
    def __init__(self, retain_height: _Optional[int] = ...) -> None: ...

class ResponseExtendVote(_message.Message):
    __slots__ = ("vote_extension",)
    VOTE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    vote_extension: bytes
    def __init__(self, vote_extension: _Optional[bytes] = ...) -> None: ...

class ResponseVerifyVoteExtension(_message.Message):
    __slots__ = ("status",)
    class VerifyStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ResponseVerifyVoteExtension.VerifyStatus]
        ACCEPT: _ClassVar[ResponseVerifyVoteExtension.VerifyStatus]
        REJECT: _ClassVar[ResponseVerifyVoteExtension.VerifyStatus]
    UNKNOWN: ResponseVerifyVoteExtension.VerifyStatus
    ACCEPT: ResponseVerifyVoteExtension.VerifyStatus
    REJECT: ResponseVerifyVoteExtension.VerifyStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ResponseVerifyVoteExtension.VerifyStatus
    def __init__(self, status: _Optional[_Union[ResponseVerifyVoteExtension.VerifyStatus, str]] = ...) -> None: ...

class ResponseFinalizeBlock(_message.Message):
    __slots__ = ("events", "tx_results", "validator_updates", "consensus_param_updates", "app_hash")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    TX_RESULTS_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_UPDATES_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_PARAM_UPDATES_FIELD_NUMBER: _ClassVar[int]
    APP_HASH_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_types_pb2_1.Event]
    tx_results: _containers.RepeatedCompositeFieldContainer[ExecTxResult]
    validator_updates: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    consensus_param_updates: _params_pb2.ConsensusParams
    app_hash: bytes
    def __init__(self, events: _Optional[_Iterable[_Union[_types_pb2_1.Event, _Mapping]]] = ..., tx_results: _Optional[_Iterable[_Union[ExecTxResult, _Mapping]]] = ..., validator_updates: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]] = ..., consensus_param_updates: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]] = ..., app_hash: _Optional[bytes] = ...) -> None: ...

class VoteInfo(_message.Message):
    __slots__ = ("validator", "block_id_flag")
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    BLOCK_ID_FLAG_FIELD_NUMBER: _ClassVar[int]
    validator: _types_pb2.Validator
    block_id_flag: _validator_pb2.BlockIDFlag
    def __init__(self, validator: _Optional[_Union[_types_pb2.Validator, _Mapping]] = ..., block_id_flag: _Optional[_Union[_validator_pb2.BlockIDFlag, str]] = ...) -> None: ...

class ExtendedVoteInfo(_message.Message):
    __slots__ = ("validator", "vote_extension", "extension_signature", "block_id_flag")
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    VOTE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    BLOCK_ID_FLAG_FIELD_NUMBER: _ClassVar[int]
    validator: _types_pb2.Validator
    vote_extension: bytes
    extension_signature: bytes
    block_id_flag: _validator_pb2.BlockIDFlag
    def __init__(self, validator: _Optional[_Union[_types_pb2.Validator, _Mapping]] = ..., vote_extension: _Optional[bytes] = ..., extension_signature: _Optional[bytes] = ..., block_id_flag: _Optional[_Union[_validator_pb2.BlockIDFlag, str]] = ...) -> None: ...

class CommitInfo(_message.Message):
    __slots__ = ("round", "votes")
    ROUND_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    round: int
    votes: _containers.RepeatedCompositeFieldContainer[VoteInfo]
    def __init__(self, round: _Optional[int] = ..., votes: _Optional[_Iterable[_Union[VoteInfo, _Mapping]]] = ...) -> None: ...

class ExtendedCommitInfo(_message.Message):
    __slots__ = ("round", "votes")
    ROUND_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    round: int
    votes: _containers.RepeatedCompositeFieldContainer[ExtendedVoteInfo]
    def __init__(self, round: _Optional[int] = ..., votes: _Optional[_Iterable[_Union[ExtendedVoteInfo, _Mapping]]] = ...) -> None: ...

class ExecTxResult(_message.Message):
    __slots__ = ("code", "data", "log", "info", "gas_wanted", "gas_used", "events", "codespace")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    GAS_WANTED_FIELD_NUMBER: _ClassVar[int]
    GAS_USED_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    CODESPACE_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: bytes
    log: str
    info: str
    gas_wanted: int
    gas_used: int
    events: _containers.RepeatedCompositeFieldContainer[_types_pb2_1.Event]
    codespace: str
    def __init__(self, code: _Optional[int] = ..., data: _Optional[bytes] = ..., log: _Optional[str] = ..., info: _Optional[str] = ..., gas_wanted: _Optional[int] = ..., gas_used: _Optional[int] = ..., events: _Optional[_Iterable[_Union[_types_pb2_1.Event, _Mapping]]] = ..., codespace: _Optional[str] = ...) -> None: ...

class TxResult(_message.Message):
    __slots__ = ("height", "index", "tx", "result")
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TX_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    height: int
    index: int
    tx: bytes
    result: ExecTxResult
    def __init__(self, height: _Optional[int] = ..., index: _Optional[int] = ..., tx: _Optional[bytes] = ..., result: _Optional[_Union[ExecTxResult, _Mapping]] = ...) -> None: ...
