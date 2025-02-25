from ibc.core.channel.v1 import channel_pb2 as _channel_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryAppVersionRequest(_message.Message):
    __slots__ = ("port_id", "connection_id", "ordering", "counterparty", "proposed_version")
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ORDERING_FIELD_NUMBER: _ClassVar[int]
    COUNTERPARTY_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_VERSION_FIELD_NUMBER: _ClassVar[int]
    port_id: str
    connection_id: str
    ordering: _channel_pb2.Order
    counterparty: _channel_pb2.Counterparty
    proposed_version: str
    def __init__(self, port_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., ordering: _Optional[_Union[_channel_pb2.Order, str]] = ..., counterparty: _Optional[_Union[_channel_pb2.Counterparty, _Mapping]] = ..., proposed_version: _Optional[str] = ...) -> None: ...

class QueryAppVersionResponse(_message.Message):
    __slots__ = ("port_id", "version")
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    port_id: str
    version: str
    def __init__(self, port_id: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...
