from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Ion(_message.Message):
    __slots__ = ("id", "creator", "stake", "endpoints", "available", "capacities", "description", "slashed_times", "input_schema", "output_schema", "input_schema_hash", "output_schema_hash", "fee_per_thousand_calls")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    CAPACITIES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SLASHED_TIMES_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    INPUT_SCHEMA_HASH_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_HASH_FIELD_NUMBER: _ClassVar[int]
    FEE_PER_THOUSAND_CALLS_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    stake: int
    endpoints: _containers.RepeatedScalarFieldContainer[str]
    available: bool
    capacities: _containers.RepeatedScalarFieldContainer[str]
    description: str
    slashed_times: int
    input_schema: str
    output_schema: str
    input_schema_hash: str
    output_schema_hash: str
    fee_per_thousand_calls: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., stake: _Optional[int] = ..., endpoints: _Optional[_Iterable[str]] = ..., available: bool = ..., capacities: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., slashed_times: _Optional[int] = ..., input_schema: _Optional[str] = ..., output_schema: _Optional[str] = ..., input_schema_hash: _Optional[str] = ..., output_schema_hash: _Optional[str] = ..., fee_per_thousand_calls: _Optional[int] = ...) -> None: ...
