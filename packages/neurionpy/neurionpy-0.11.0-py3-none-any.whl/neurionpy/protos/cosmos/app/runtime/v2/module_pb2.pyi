from cosmos.app.v1alpha1 import module_pb2 as _module_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Module(_message.Message):
    __slots__ = ("app_name", "pre_blockers", "begin_blockers", "end_blockers", "tx_validators", "init_genesis", "export_genesis", "order_migrations", "gas_config", "override_store_keys", "skip_store_keys")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    PRE_BLOCKERS_FIELD_NUMBER: _ClassVar[int]
    BEGIN_BLOCKERS_FIELD_NUMBER: _ClassVar[int]
    END_BLOCKERS_FIELD_NUMBER: _ClassVar[int]
    TX_VALIDATORS_FIELD_NUMBER: _ClassVar[int]
    INIT_GENESIS_FIELD_NUMBER: _ClassVar[int]
    EXPORT_GENESIS_FIELD_NUMBER: _ClassVar[int]
    ORDER_MIGRATIONS_FIELD_NUMBER: _ClassVar[int]
    GAS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_STORE_KEYS_FIELD_NUMBER: _ClassVar[int]
    SKIP_STORE_KEYS_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    pre_blockers: _containers.RepeatedScalarFieldContainer[str]
    begin_blockers: _containers.RepeatedScalarFieldContainer[str]
    end_blockers: _containers.RepeatedScalarFieldContainer[str]
    tx_validators: _containers.RepeatedScalarFieldContainer[str]
    init_genesis: _containers.RepeatedScalarFieldContainer[str]
    export_genesis: _containers.RepeatedScalarFieldContainer[str]
    order_migrations: _containers.RepeatedScalarFieldContainer[str]
    gas_config: GasConfig
    override_store_keys: _containers.RepeatedCompositeFieldContainer[StoreKeyConfig]
    skip_store_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app_name: _Optional[str] = ..., pre_blockers: _Optional[_Iterable[str]] = ..., begin_blockers: _Optional[_Iterable[str]] = ..., end_blockers: _Optional[_Iterable[str]] = ..., tx_validators: _Optional[_Iterable[str]] = ..., init_genesis: _Optional[_Iterable[str]] = ..., export_genesis: _Optional[_Iterable[str]] = ..., order_migrations: _Optional[_Iterable[str]] = ..., gas_config: _Optional[_Union[GasConfig, _Mapping]] = ..., override_store_keys: _Optional[_Iterable[_Union[StoreKeyConfig, _Mapping]]] = ..., skip_store_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class GasConfig(_message.Message):
    __slots__ = ("validate_tx_gas_limit", "query_gas_limit", "simulation_gas_limit")
    VALIDATE_TX_GAS_LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUERY_GAS_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_GAS_LIMIT_FIELD_NUMBER: _ClassVar[int]
    validate_tx_gas_limit: int
    query_gas_limit: int
    simulation_gas_limit: int
    def __init__(self, validate_tx_gas_limit: _Optional[int] = ..., query_gas_limit: _Optional[int] = ..., simulation_gas_limit: _Optional[int] = ...) -> None: ...

class StoreKeyConfig(_message.Message):
    __slots__ = ("module_name", "kv_store_key")
    MODULE_NAME_FIELD_NUMBER: _ClassVar[int]
    KV_STORE_KEY_FIELD_NUMBER: _ClassVar[int]
    module_name: str
    kv_store_key: str
    def __init__(self, module_name: _Optional[str] = ..., kv_store_key: _Optional[str] = ...) -> None: ...
