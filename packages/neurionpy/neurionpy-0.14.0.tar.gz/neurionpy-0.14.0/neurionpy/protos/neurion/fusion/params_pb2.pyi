from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ("admin_address", "min_task_reward", "min_task_proposer_stake", "min_task_validator_stake", "min_proposal_duration_in_seconds", "min_dispute_duration_in_seconds", "min_creator_stake", "creator_application_fee", "dispute_validator_reward", "min_dispute_score_deposit", "first_proposer_weight", "second_proposer_weight", "third_proposer_weight", "proposer_reward_percentage", "validator_reward_percentage", "staker_reward_percentage")
    ADMIN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_REWARD_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_PROPOSER_STAKE_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_VALIDATOR_STAKE_FIELD_NUMBER: _ClassVar[int]
    MIN_PROPOSAL_DURATION_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MIN_DISPUTE_DURATION_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATOR_STAKE_FIELD_NUMBER: _ClassVar[int]
    CREATOR_APPLICATION_FEE_FIELD_NUMBER: _ClassVar[int]
    DISPUTE_VALIDATOR_REWARD_FIELD_NUMBER: _ClassVar[int]
    MIN_DISPUTE_SCORE_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    FIRST_PROPOSER_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    SECOND_PROPOSER_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    THIRD_PROPOSER_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    STAKER_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    admin_address: str
    min_task_reward: int
    min_task_proposer_stake: int
    min_task_validator_stake: int
    min_proposal_duration_in_seconds: int
    min_dispute_duration_in_seconds: int
    min_creator_stake: int
    creator_application_fee: int
    dispute_validator_reward: int
    min_dispute_score_deposit: int
    first_proposer_weight: int
    second_proposer_weight: int
    third_proposer_weight: int
    proposer_reward_percentage: int
    validator_reward_percentage: int
    staker_reward_percentage: int
    def __init__(self, admin_address: _Optional[str] = ..., min_task_reward: _Optional[int] = ..., min_task_proposer_stake: _Optional[int] = ..., min_task_validator_stake: _Optional[int] = ..., min_proposal_duration_in_seconds: _Optional[int] = ..., min_dispute_duration_in_seconds: _Optional[int] = ..., min_creator_stake: _Optional[int] = ..., creator_application_fee: _Optional[int] = ..., dispute_validator_reward: _Optional[int] = ..., min_dispute_score_deposit: _Optional[int] = ..., first_proposer_weight: _Optional[int] = ..., second_proposer_weight: _Optional[int] = ..., third_proposer_weight: _Optional[int] = ..., proposer_reward_percentage: _Optional[int] = ..., validator_reward_percentage: _Optional[int] = ..., staker_reward_percentage: _Optional[int] = ...) -> None: ...
