from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Pathway(_message.Message):
    __slots__ = ("id", "creator", "name", "description", "is_public", "ions", "fee_per_thousand_calls", "field_maps", "stake")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    IONS_FIELD_NUMBER: _ClassVar[int]
    FEE_PER_THOUSAND_CALLS_FIELD_NUMBER: _ClassVar[int]
    FIELD_MAPS_FIELD_NUMBER: _ClassVar[int]
    STAKE_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    name: str
    description: str
    is_public: bool
    ions: _containers.RepeatedScalarFieldContainer[str]
    fee_per_thousand_calls: int
    field_maps: _containers.RepeatedScalarFieldContainer[str]
    stake: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_public: bool = ..., ions: _Optional[_Iterable[str]] = ..., fee_per_thousand_calls: _Optional[int] = ..., field_maps: _Optional[_Iterable[str]] = ..., stake: _Optional[int] = ...) -> None: ...
