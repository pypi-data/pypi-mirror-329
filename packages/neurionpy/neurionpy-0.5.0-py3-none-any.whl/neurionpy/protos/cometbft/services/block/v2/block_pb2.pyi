from cometbft.types.v2 import types_pb2 as _types_pb2
from cometbft.types.v2 import block_pb2 as _block_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetByHeightRequest(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...

class GetByHeightResponse(_message.Message):
    __slots__ = ("block_id", "block")
    BLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    block_id: _types_pb2.BlockID
    block: _block_pb2.Block
    def __init__(self, block_id: _Optional[_Union[_types_pb2.BlockID, _Mapping]] = ..., block: _Optional[_Union[_block_pb2.Block, _Mapping]] = ...) -> None: ...

class GetLatestHeightRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLatestHeightResponse(_message.Message):
    __slots__ = ("height",)
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    height: int
    def __init__(self, height: _Optional[int] = ...) -> None: ...
