from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Txs(_message.Message):
    __slots__ = ("txs",)
    TXS_FIELD_NUMBER: _ClassVar[int]
    txs: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, txs: _Optional[_Iterable[bytes]] = ...) -> None: ...

class HaveTx(_message.Message):
    __slots__ = ("tx_key",)
    TX_KEY_FIELD_NUMBER: _ClassVar[int]
    tx_key: bytes
    def __init__(self, tx_key: _Optional[bytes] = ...) -> None: ...

class ResetRoute(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Message(_message.Message):
    __slots__ = ("txs", "have_tx", "reset_route")
    TXS_FIELD_NUMBER: _ClassVar[int]
    HAVE_TX_FIELD_NUMBER: _ClassVar[int]
    RESET_ROUTE_FIELD_NUMBER: _ClassVar[int]
    txs: Txs
    have_tx: HaveTx
    reset_route: ResetRoute
    def __init__(self, txs: _Optional[_Union[Txs, _Mapping]] = ..., have_tx: _Optional[_Union[HaveTx, _Mapping]] = ..., reset_route: _Optional[_Union[ResetRoute, _Mapping]] = ...) -> None: ...
