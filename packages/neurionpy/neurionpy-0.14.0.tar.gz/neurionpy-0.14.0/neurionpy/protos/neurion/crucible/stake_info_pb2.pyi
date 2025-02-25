from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StakeInfo(_message.Message):
    __slots__ = ("amount", "last_update_time", "weighted_stake")
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    WEIGHTED_STAKE_FIELD_NUMBER: _ClassVar[int]
    amount: str
    last_update_time: int
    weighted_stake: str
    def __init__(self, amount: _Optional[str] = ..., last_update_time: _Optional[int] = ..., weighted_stake: _Optional[str] = ...) -> None: ...
