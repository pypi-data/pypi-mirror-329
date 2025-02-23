from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Snapshot(_message.Message):
    __slots__ = ("height", "format", "chunks", "hash", "metadata")
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    height: int
    format: int
    chunks: int
    hash: bytes
    metadata: Metadata
    def __init__(self, height: _Optional[int] = ..., format: _Optional[int] = ..., chunks: _Optional[int] = ..., hash: _Optional[bytes] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("chunk_hashes",)
    CHUNK_HASHES_FIELD_NUMBER: _ClassVar[int]
    chunk_hashes: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, chunk_hashes: _Optional[_Iterable[bytes]] = ...) -> None: ...
