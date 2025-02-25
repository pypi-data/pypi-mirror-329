from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ("min_ion_stake", "max_number_of_slashes", "slash_ratio_percentage", "minimum_reporting_fee", "admin_address", "protocol_surcharge_ratio_percentage", "fee_increase_cooloff_period", "max_fee_increase_ratio_percentage", "stakers_reward_percentage", "pathway_owner_rebate_percentage", "pathway_min_stake")
    MIN_ION_STAKE_FIELD_NUMBER: _ClassVar[int]
    MAX_NUMBER_OF_SLASHES_FIELD_NUMBER: _ClassVar[int]
    SLASH_RATIO_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_REPORTING_FEE_FIELD_NUMBER: _ClassVar[int]
    ADMIN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_SURCHARGE_RATIO_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    FEE_INCREASE_COOLOFF_PERIOD_FIELD_NUMBER: _ClassVar[int]
    MAX_FEE_INCREASE_RATIO_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    STAKERS_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    PATHWAY_OWNER_REBATE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    PATHWAY_MIN_STAKE_FIELD_NUMBER: _ClassVar[int]
    min_ion_stake: int
    max_number_of_slashes: int
    slash_ratio_percentage: int
    minimum_reporting_fee: int
    admin_address: str
    protocol_surcharge_ratio_percentage: int
    fee_increase_cooloff_period: int
    max_fee_increase_ratio_percentage: int
    stakers_reward_percentage: int
    pathway_owner_rebate_percentage: int
    pathway_min_stake: int
    def __init__(self, min_ion_stake: _Optional[int] = ..., max_number_of_slashes: _Optional[int] = ..., slash_ratio_percentage: _Optional[int] = ..., minimum_reporting_fee: _Optional[int] = ..., admin_address: _Optional[str] = ..., protocol_surcharge_ratio_percentage: _Optional[int] = ..., fee_increase_cooloff_period: _Optional[int] = ..., max_fee_increase_ratio_percentage: _Optional[int] = ..., stakers_reward_percentage: _Optional[int] = ..., pathway_owner_rebate_percentage: _Optional[int] = ..., pathway_min_stake: _Optional[int] = ...) -> None: ...
