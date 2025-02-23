from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StoreKVPair(_message.Message):
    __slots__ = ("store_key", "delete", "key", "value")
    STORE_KEY_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    store_key: str
    delete: bool
    key: bytes
    value: bytes
    def __init__(self, store_key: _Optional[str] = ..., delete: bool = ..., key: _Optional[bytes] = ..., value: _Optional[bytes] = ...) -> None: ...
