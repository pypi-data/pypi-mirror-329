from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ("min_dataset_stake", "min_dataset_fee", "admin_address", "protocol_fee", "protocol_deposit", "request_processing_fee", "staker_reward_percentage")
    MIN_DATASET_STAKE_FIELD_NUMBER: _ClassVar[int]
    MIN_DATASET_FEE_FIELD_NUMBER: _ClassVar[int]
    ADMIN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FEE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_PROCESSING_FEE_FIELD_NUMBER: _ClassVar[int]
    STAKER_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    min_dataset_stake: int
    min_dataset_fee: int
    admin_address: str
    protocol_fee: int
    protocol_deposit: int
    request_processing_fee: int
    staker_reward_percentage: int
    def __init__(self, min_dataset_stake: _Optional[int] = ..., min_dataset_fee: _Optional[int] = ..., admin_address: _Optional[str] = ..., protocol_fee: _Optional[int] = ..., protocol_deposit: _Optional[int] = ..., request_processing_fee: _Optional[int] = ..., staker_reward_percentage: _Optional[int] = ...) -> None: ...
