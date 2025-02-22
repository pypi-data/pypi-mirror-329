from cometbft.abci.v2 import types_pb2 as _types_pb2
from cometbft.types.v2 import params_pb2 as _params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetBlockResultsRequest(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...

class GetBlockResultsResponse(_message.Message):
    __slots__ = ("height", "tx_results", "finalize_block_events", "validator_updates", "consensus_param_updates", "app_hash")
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TX_RESULTS_FIELD_NUMBER: _ClassVar[int]
    FINALIZE_BLOCK_EVENTS_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_UPDATES_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_PARAM_UPDATES_FIELD_NUMBER: _ClassVar[int]
    APP_HASH_FIELD_NUMBER: _ClassVar[int]
    height: int
    tx_results: _containers.RepeatedCompositeFieldContainer[_types_pb2.ExecTxResult]
    finalize_block_events: _containers.RepeatedCompositeFieldContainer[_types_pb2.Event]
    validator_updates: _containers.RepeatedCompositeFieldContainer[_types_pb2.ValidatorUpdate]
    consensus_param_updates: _params_pb2.ConsensusParams
    app_hash: bytes
    def __init__(self, height: _Optional[int] = ..., tx_results: _Optional[_Iterable[_Union[_types_pb2.ExecTxResult, _Mapping]]] = ..., finalize_block_events: _Optional[_Iterable[_Union[_types_pb2.Event, _Mapping]]] = ..., validator_updates: _Optional[_Iterable[_Union[_types_pb2.ValidatorUpdate, _Mapping]]] = ..., consensus_param_updates: _Optional[_Union[_params_pb2.ConsensusParams, _Mapping]] = ..., app_hash: _Optional[bytes] = ...) -> None: ...
