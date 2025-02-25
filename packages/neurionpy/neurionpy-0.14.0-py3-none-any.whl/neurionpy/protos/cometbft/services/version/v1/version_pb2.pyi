from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetVersionRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetVersionResponse(_message.Message):
    __slots__ = ("node", "abci", "p2p", "block")
    NODE_FIELD_NUMBER: _ClassVar[int]
    ABCI_FIELD_NUMBER: _ClassVar[int]
    P2P_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    node: str
    abci: str
    p2p: int
    block: int
    def __init__(self, node: _Optional[str] = ..., abci: _Optional[str] = ..., p2p: _Optional[int] = ..., block: _Optional[int] = ...) -> None: ...
