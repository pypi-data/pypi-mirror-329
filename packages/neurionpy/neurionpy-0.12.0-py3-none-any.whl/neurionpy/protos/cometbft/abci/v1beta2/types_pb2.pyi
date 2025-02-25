from gogoproto import gogo_pb2 as _gogo_pb2
from cometbft.abci.v1beta1 import types_pb2 as _types_pb2
from cometbft.types.v1beta1 import types_pb2 as _types_pb2_1
from cometbft.types.v1beta2 import params_pb2 as _params_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MisbehaviorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[MisbehaviorType]
    DUPLICATE_VOTE: _ClassVar[MisbehaviorType]
    LIGHT_CLIENT_ATTACK: _ClassVar[MisbehaviorType]
UNKNOWN: MisbehaviorType
DUPLICATE_VOTE: MisbehaviorType
LIGHT_CLIENT_ATTACK: MisbehaviorType

class Request(_message.Message):
    __slots__ = ("echo", "flush", "info", "init_chain", "query", "begin_block", "check_tx", "deliver_tx", "end_block", "commit", "list_snapshots", "offer_snapshot", "load_snapshot_chunk", "apply_snapshot_chunk", "prepare_proposal", "process_proposal")
    ECHO_FIELD_NUMBER: _ClassVar[int]
    FLUSH_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    INIT_CHAIN_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    BEGIN_BLOCK_FIELD_NUMBER: _ClassVar[int]
    CHECK_TX_FIELD_NUMBER: _ClassVar[int]
    DELIVER_TX_FIELD_NUMBER: _ClassVar[int]
    END_BLOCK_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    LIST_SNAPSHOTS_FIELD_NUMBER: _ClassVar[int]
    OFFER_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    LOAD_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    APPLY_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    PREPARE_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    PROCESS_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    echo: _types_pb2.RequestEcho
    flush: _types_pb2.RequestFlush
    info: RequestInfo
    init_chain: RequestInitChain
    query: _types_pb2.RequestQuery
    begin_block: RequestBeginBlock
    check_tx: _types_pb2.RequestCheckTx
    deliver_tx: _types_pb2.RequestDeliverTx
    end_block: _types_pb2.RequestEndBlock
    commit: _types_pb2.RequestCommit
    list_snapshots: _types_pb2.RequestListSnapshots
    offer_snapshot: _types_pb2.RequestOfferSnapshot
    load_snapshot_chunk: _types_pb2.RequestLoadSnapshotChunk
    apply_snapshot_chunk: _types_pb2.RequestApplySnapshotChunk
    prepare_proposal: RequestPrepareProposal
    process_proposal: RequestProcessProposal
    def __init__(self, echo: _Optional[_Union[_types_pb2.RequestEcho, _Mapping]] = ..., flush: _Optional[_Union[_types_pb2.RequestFlush, _Mapping]] = ..., info: _Optional[_Union[RequestInfo, _Mapping]] = ..., init_chain: _Optional[_Union[RequestInitChain, _Mapping]] = ..., query: _Optional[_Union[_types_pb2.RequestQuery, _Mapping]] = ..., begin_block: _Optional[_Union[RequestBeginBlock, _Mapping]] = ..., check_tx: _Optional[_Union[_types_pb2.RequestCheckTx, _Mapping]] = ..., deliver_tx: _Optional[_Union[_types_pb2.RequestDeliverTx, _Mapping]] = ..., end_block: _Optional[_Union[_types_pb2.RequestEndBlock, _Mapping]] = ..., commit: _Optional[_Union[_types_pb2.RequestCommit, _Mapping]] = ..., list_snapshots: _Optional[_Union[_types_pb2.RequestListSnapshots, _Mapping]] = ..., offer_snapshot: _Optional[_Union[_types_pb2.RequestOfferSnapshot, _Mapping]] = ..., load_snapshot_chunk: _Optional[_Union[_types_pb2.RequestLoadSnapshotChunk, _Mapping]] = ..., apply_snapshot_chunk: _Optional[_Union[_types_pb2.RequestApplySnapshotChunk, _Mapping]] = ..., prepare_proposal: _Optional[_Union[RequestPrepareProposal, _Mapping]] = ..., process_proposal: _Optional[_Union[RequestProcessProposal, _Mapping]] = ...) -> None: ...

class RequestInfo(_message.Message):
    __slots__ = ("version", "block_version", "p2p_version", "abci_version")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BLOCK_VERSION_FIELD_NUMBER: _ClassVar[int]
    P2P_VERSION_FIELD_NUMBER: _ClassVar[int]
    ABCI_VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    block_version: int
    p2p_version: int
    abci_version: str
    def __init__(self, version: _Optional[str] = ..., block_version: _Optional[int] = ..., p2p_version: _Optional[int] = ..., abci_version: _Optional[str] = ...) -> None: ...

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

class RequestBeginBlock(_message.Message):
    __slots__ = ("hash", "header", "last_commit_info", "byzantine_validators")
    HASH_FIELD_NUMBER: _ClassVar[int]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LAST_COMMIT_INFO_FIELD_NUMBER: _ClassVar[int]
    BYZANTINE_VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    header: _types_pb2_1.Header
    last_commit_info: CommitInfo
    byzantine_validators: _containers.RepeatedCompositeFieldContainer[Misbehavior]
    def __init__(self, hash: _Optional[bytes] = ..., header: _Optional[_Union[_types_pb2_1.Header, _Mapping]] = ..., last_commit_info: _Optional[_Union[CommitInfo, _Mapping]] = ..., byzantine_validators: _Optional[_Iterable[_Union[Misbehavior, _Mapping]]] = ...) -> None: ...

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
    misbehavior: _containers.RepeatedCompositeFieldContainer[Misbehavior]
    height: int
    time: _timestamp_pb2.Timestamp
    next_validators_hash: bytes
    proposer_address: bytes
    def __init__(self, max_tx_bytes: _Optional[int] = ..., txs: _Optional[_Iterable[bytes]] = ..., local_last_commit: _Optional[_Union[ExtendedCommitInfo, _Mapping]] = ..., misbehavior: _Optional[_Iterable[_Union[Misbehavior, _Mapping]]] = ..., height: _Optional[int] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., next_validators_hash: _Optional[bytes] = ..., proposer_address: _Optional[bytes] = ...) -> None: ...

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
    misbehavior: _containers.RepeatedCompositeFieldContainer[Misbehavior]
    hash: bytes
    height: int
    time: _timestamp_pb2.Timestamp
    next_validators_hash: bytes
    proposer_address: bytes
    def __init__(self, txs: _Optional[_Iterable[bytes]] = ..., proposed_last_commit: _Optional[_Union[CommitInfo, _Mapping]] = ..., misbehavior: _Optional[_Iterable[_Union[Misbehavior, _Mapping]]] = ..., hash: _Optional[bytes] = ..., height: _Optional[int] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., next_validators_hash: _Optional[bytes] = ..., proposer_address: _Optional[bytes] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("exception", "echo", "flush", "info", "init_chain", "query", "begin_block", "check_tx", "deliver_tx", "end_block", "commit", "list_snapshots", "offer_snapshot", "load_snapshot_chunk", "apply_snapshot_chunk", "prepare_proposal", "process_proposal")
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    FLUSH_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    INIT_CHAIN_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    BEGIN_BLOCK_FIELD_NUMBER: _ClassVar[int]
    CHECK_TX_FIELD_NUMBER: _ClassVar[int]
    DELIVER_TX_FIELD_NUMBER: _ClassVar[int]
    END_BLOCK_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    LIST_SNAPSHOTS_FIELD_NUMBER: _ClassVar[int]
    OFFER_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    LOAD_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    APPLY_SNAPSHOT_CHUNK_FIELD_NUMBER: _ClassVar[int]
    PREPARE_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    PROCESS_PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    exception: _types_pb2.ResponseException
    echo: _types_pb2.ResponseEcho
    flush: _types_pb2.ResponseFlush
    info: _types_pb2.ResponseInfo
    init_chain: ResponseInitChain
    query: _types_pb2.ResponseQuery
    begin_block: ResponseBeginBlock
    check_tx: ResponseCheckTx
    deliver_tx: ResponseDeliverTx
    end_block: ResponseEndBlock
    commit: _types_pb2.ResponseCommit
    list_snapshots: _types_pb2.ResponseListSnapshots
    offer_snapshot: _types_pb2.ResponseOfferSnapshot
    load_snapshot_chunk: _types_pb2.ResponseLoadSnapshotChunk
    apply_snapshot_chunk: _types_pb2.ResponseApplySnapshotChunk
    prepare_proposal: ResponsePrepareProposal
    process_proposal: ResponseProcessProposal
    def __init__(self, exception: _Optional[_Union[_types_pb2.ResponseException, _Mapping]] = ..., echo: _Optional[_Union[_types_pb2.ResponseEcho, _Mapping]] = ..., flush: _Optional[_Union[_types_pb2.ResponseFlush, _Mapping]] = ..., info: _Optional[_Union[_types_pb2.ResponseInfo, _Mapping]] = ..., init_chain: _Optional[_Union[ResponseInitChain, _Mapping]] = ..., query: _Optional[_Union[_types_pb2.ResponseQuery, _Mapping]] = ..., begin_block: _Optional[_Union[ResponseBeginBlock, _Mapping]] = ..., check_tx: _Optional[_Union[ResponseCheckTx, _Mapping]] = ..., deliver_tx: _Optional[_Union[ResponseDeliverTx, _Mapping]] = ..., end_block: _Optional[_Union[ResponseEndBlock, _Mapping]] = ..., commit: _Optional[_Union[_types_pb2.ResponseCommit, _Mapping]] = ..., list_snapshots: _Optional[_Union[_types_pb2.ResponseListSnapshots, _Mapping]] = ..., offer_snapshot: _Optional[_Union[_types_pb2.ResponseOfferSnapshot, _Mapping]] = ..., load_snapshot_chunk: _Optional[_Union[_types_pb2.ResponseLoadSnapshotChunk, _Mapping]] = ..., apply_snapshot_chunk: _Optional[_Union[_types_pb2.ResponseApplySnapshotChunk, _Mapping]] = ..., prepare_proposal: _Optional[_Union[ResponsePrepareProposal, _Mapping]] = ..., process_proposal: _Optional[_Union[ResponseProcessProposal, _Mapping]] = ...) -> None: ...

class ResponseInitChain(_message.Message):
    __slots__ = ("consensus_params", "validators", "app_hash")
    CONSENSUS_PARAMS_FIELD_NUMBER: _ClassVar[int]
    VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    APP_HASH_FIELD_NUMBER: _ClassVar[int]
    consensus_params: _params_pb2.ConsensusParams
    validators: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    app_hash: bytes
    def __init__(self, consensus_params: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]] = ..., validators: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]] = ..., app_hash: _Optional[bytes] = ...) -> None: ...

class ResponseBeginBlock(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(self, events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...) -> None: ...

class ResponseCheckTx(_message.Message):
    __slots__ = ("code", "data", "log", "info", "gas_wanted", "gas_used", "events", "codespace", "sender", "priority", "mempool_error")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    GAS_WANTED_FIELD_NUMBER: _ClassVar[int]
    GAS_USED_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    CODESPACE_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    MEMPOOL_ERROR_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: bytes
    log: str
    info: str
    gas_wanted: int
    gas_used: int
    events: _containers.RepeatedCompositeFieldContainer[Event]
    codespace: str
    sender: str
    priority: int
    mempool_error: str
    def __init__(self, code: _Optional[int] = ..., data: _Optional[bytes] = ..., log: _Optional[str] = ..., info: _Optional[str] = ..., gas_wanted: _Optional[int] = ..., gas_used: _Optional[int] = ..., events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ..., codespace: _Optional[str] = ..., sender: _Optional[str] = ..., priority: _Optional[int] = ..., mempool_error: _Optional[str] = ...) -> None: ...

class ResponseDeliverTx(_message.Message):
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
    events: _containers.RepeatedCompositeFieldContainer[Event]
    codespace: str
    def __init__(self, code: _Optional[int] = ..., data: _Optional[bytes] = ..., log: _Optional[str] = ..., info: _Optional[str] = ..., gas_wanted: _Optional[int] = ..., gas_used: _Optional[int] = ..., events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ..., codespace: _Optional[str] = ...) -> None: ...

class ResponseEndBlock(_message.Message):
    __slots__ = ("validator_updates", "consensus_param_updates", "events")
    VALIDATOR_UPDATES_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_PARAM_UPDATES_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    validator_updates: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    consensus_param_updates: _params_pb2.ConsensusParams
    events: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(self, validator_updates: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]] = ..., consensus_param_updates: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]] = ..., events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...) -> None: ...

class ResponsePrepareProposal(_message.Message):
    __slots__ = ("txs",)
    TXS_FIELD_NUMBER: _ClassVar[int]
    txs: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, txs: _Optional[_Iterable[bytes]] = ...) -> None: ...

class ResponseProcessProposal(_message.Message):
    __slots__ = ("status",)
    class ProposalStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ResponseProcessProposal.ProposalStatus]
        ACCEPT: _ClassVar[ResponseProcessProposal.ProposalStatus]
        REJECT: _ClassVar[ResponseProcessProposal.ProposalStatus]
    UNKNOWN: ResponseProcessProposal.ProposalStatus
    ACCEPT: ResponseProcessProposal.ProposalStatus
    REJECT: ResponseProcessProposal.ProposalStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ResponseProcessProposal.ProposalStatus
    def __init__(self, status: _Optional[_Union[ResponseProcessProposal.ProposalStatus, str]] = ...) -> None: ...

class CommitInfo(_message.Message):
    __slots__ = ("round", "votes")
    ROUND_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    round: int
    votes: _containers.RepeatedCompositeFieldContainer[_types_pb2.VoteInfo]
    def __init__(self, round: _Optional[int] = ..., votes: _Optional[_Iterable[_Union[_types_pb2.VoteInfo, _Mapping]]] = ...) -> None: ...

class ExtendedCommitInfo(_message.Message):
    __slots__ = ("round", "votes")
    ROUND_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    round: int
    votes: _containers.RepeatedCompositeFieldContainer[ExtendedVoteInfo]
    def __init__(self, round: _Optional[int] = ..., votes: _Optional[_Iterable[_Union[ExtendedVoteInfo, _Mapping]]] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("type", "attributes")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    type: str
    attributes: _containers.RepeatedCompositeFieldContainer[EventAttribute]
    def __init__(self, type: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[EventAttribute, _Mapping]]] = ...) -> None: ...

class EventAttribute(_message.Message):
    __slots__ = ("key", "value", "index")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    index: bool
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ..., index: bool = ...) -> None: ...

class ExtendedVoteInfo(_message.Message):
    __slots__ = ("validator", "signed_last_block", "vote_extension")
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    SIGNED_LAST_BLOCK_FIELD_NUMBER: _ClassVar[int]
    VOTE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    validator: _types_pb2.Validator
    signed_last_block: bool
    vote_extension: bytes
    def __init__(self, validator: _Optional[_Union[_types_pb2.Validator, _Mapping]] = ..., signed_last_block: bool = ..., vote_extension: _Optional[bytes] = ...) -> None: ...

class Misbehavior(_message.Message):
    __slots__ = ("type", "validator", "height", "time", "total_voting_power")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOTING_POWER_FIELD_NUMBER: _ClassVar[int]
    type: MisbehaviorType
    validator: _types_pb2.Validator
    height: int
    time: _timestamp_pb2.Timestamp
    total_voting_power: int
    def __init__(self, type: _Optional[_Union[MisbehaviorType, str]] = ..., validator: _Optional[_Union[_types_pb2.Validator, _Mapping]] = ..., height: _Optional[int] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., total_voting_power: _Optional[int] = ...) -> None: ...
