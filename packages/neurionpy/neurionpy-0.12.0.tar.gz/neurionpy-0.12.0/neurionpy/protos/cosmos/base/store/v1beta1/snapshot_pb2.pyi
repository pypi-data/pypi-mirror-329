from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SnapshotItem(_message.Message):
    __slots__ = ("store", "iavl")
    STORE_FIELD_NUMBER: _ClassVar[int]
    IAVL_FIELD_NUMBER: _ClassVar[int]
    store: SnapshotStoreItem
    iavl: SnapshotIAVLItem
    def __init__(self, store: _Optional[_Union[SnapshotStoreItem, _Mapping]] = ..., iavl: _Optional[_Union[SnapshotIAVLItem, _Mapping]] = ...) -> None: ...

class SnapshotStoreItem(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class SnapshotIAVLItem(_message.Message):
    __slots__ = ("key", "value", "version", "height")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    value: bytes
    version: int
    height: int
    def __init__(self, key: _Optional[bytes] = ..., value: _Optional[bytes] = ..., version: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
