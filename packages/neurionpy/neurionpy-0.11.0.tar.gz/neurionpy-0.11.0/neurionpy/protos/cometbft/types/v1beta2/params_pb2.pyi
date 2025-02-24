from gogoproto import gogo_pb2 as _gogo_pb2
from cometbft.types.v1beta1 import params_pb2 as _params_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConsensusParams(_message.Message):
    __slots__ = ("block", "evidence", "validator", "version")
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    EVIDENCE_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    block: BlockParams
    evidence: _params_pb2.EvidenceParams
    validator: _params_pb2.ValidatorParams
    version: _params_pb2.VersionParams
    def __init__(self, block: _Optional[_Union[BlockParams, _Mapping]] = ..., evidence: _Optional[_Union[_params_pb2.EvidenceParams, _Mapping]] = ..., validator: _Optional[_Union[_params_pb2.ValidatorParams, _Mapping]] = ..., version: _Optional[_Union[_params_pb2.VersionParams, _Mapping]] = ...) -> None: ...

class BlockParams(_message.Message):
    __slots__ = ("max_bytes", "max_gas")
    MAX_BYTES_FIELD_NUMBER: _ClassVar[int]
    MAX_GAS_FIELD_NUMBER: _ClassVar[int]
    max_bytes: int
    max_gas: int
    def __init__(self, max_bytes: _Optional[int] = ..., max_gas: _Optional[int] = ...) -> None: ...
