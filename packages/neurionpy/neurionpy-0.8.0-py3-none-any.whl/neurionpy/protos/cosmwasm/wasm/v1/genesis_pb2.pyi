from gogoproto import gogo_pb2 as _gogo_pb2
from cosmwasm.wasm.v1 import types_pb2 as _types_pb2
from cosmwasm.wasm.v1 import tx_pb2 as _tx_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ("params", "codes", "contracts", "sequences", "gen_msgs")
    class GenMsgs(_message.Message):
        __slots__ = ("store_code", "instantiate_contract", "execute_contract")
        STORE_CODE_FIELD_NUMBER: _ClassVar[int]
        INSTANTIATE_CONTRACT_FIELD_NUMBER: _ClassVar[int]
        EXECUTE_CONTRACT_FIELD_NUMBER: _ClassVar[int]
        store_code: _tx_pb2.MsgStoreCode
        instantiate_contract: _tx_pb2.MsgInstantiateContract
        execute_contract: _tx_pb2.MsgExecuteContract
        def __init__(self, store_code: _Optional[_Union[_tx_pb2.MsgStoreCode, _Mapping]] = ..., instantiate_contract: _Optional[_Union[_tx_pb2.MsgInstantiateContract, _Mapping]] = ..., execute_contract: _Optional[_Union[_tx_pb2.MsgExecuteContract, _Mapping]] = ...) -> None: ...
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    CODES_FIELD_NUMBER: _ClassVar[int]
    CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    GEN_MSGS_FIELD_NUMBER: _ClassVar[int]
    params: _types_pb2.Params
    codes: _containers.RepeatedCompositeFieldContainer[Code]
    contracts: _containers.RepeatedCompositeFieldContainer[Contract]
    sequences: _containers.RepeatedCompositeFieldContainer[Sequence]
    gen_msgs: _containers.RepeatedCompositeFieldContainer[GenesisState.GenMsgs]
    def __init__(self, params: _Optional[_Union[_types_pb2.Params, _Mapping]] = ..., codes: _Optional[_Iterable[_Union[Code, _Mapping]]] = ..., contracts: _Optional[_Iterable[_Union[Contract, _Mapping]]] = ..., sequences: _Optional[_Iterable[_Union[Sequence, _Mapping]]] = ..., gen_msgs: _Optional[_Iterable[_Union[GenesisState.GenMsgs, _Mapping]]] = ...) -> None: ...

class Code(_message.Message):
    __slots__ = ("code_id", "code_info", "code_bytes", "pinned")
    CODE_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_INFO_FIELD_NUMBER: _ClassVar[int]
    CODE_BYTES_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    code_id: int
    code_info: _types_pb2.CodeInfo
    code_bytes: bytes
    pinned: bool
    def __init__(self, code_id: _Optional[int] = ..., code_info: _Optional[_Union[_types_pb2.CodeInfo, _Mapping]] = ..., code_bytes: _Optional[bytes] = ..., pinned: bool = ...) -> None: ...

class Contract(_message.Message):
    __slots__ = ("contract_address", "contract_info", "contract_state")
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_INFO_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_STATE_FIELD_NUMBER: _ClassVar[int]
    contract_address: str
    contract_info: _types_pb2.ContractInfo
    contract_state: _containers.RepeatedCompositeFieldContainer[_types_pb2.Model]
    def __init__(self, contract_address: _Optional[str] = ..., contract_info: _Optional[_Union[_types_pb2.ContractInfo, _Mapping]] = ..., contract_state: _Optional[_Iterable[_Union[_types_pb2.Model, _Mapping]]] = ...) -> None: ...

class Sequence(_message.Message):
    __slots__ = ("id_key", "value")
    ID_KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    id_key: bytes
    value: int
    def __init__(self, id_key: _Optional[bytes] = ..., value: _Optional[int] = ...) -> None: ...
