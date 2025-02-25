from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Minter(_message.Message):
    __slots__ = ("inflation", "annual_provisions")
    INFLATION_FIELD_NUMBER: _ClassVar[int]
    ANNUAL_PROVISIONS_FIELD_NUMBER: _ClassVar[int]
    inflation: str
    annual_provisions: str
    def __init__(self, inflation: _Optional[str] = ..., annual_provisions: _Optional[str] = ...) -> None: ...

class Params(_message.Message):
    __slots__ = ("mint_denom", "inflation_rate", "blocks_per_year")
    MINT_DENOM_FIELD_NUMBER: _ClassVar[int]
    INFLATION_RATE_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_PER_YEAR_FIELD_NUMBER: _ClassVar[int]
    mint_denom: str
    inflation_rate: str
    blocks_per_year: int
    def __init__(self, mint_denom: _Optional[str] = ..., inflation_rate: _Optional[str] = ..., blocks_per_year: _Optional[int] = ...) -> None: ...
