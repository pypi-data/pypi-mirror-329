from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ("admin_address", "min_task_duration_in_days", "min_task_reward", "min_task_trainer_stake", "min_task_scorer_stake", "submission_cooling_off_period_in_seconds", "min_report_plagiarism_deposit", "min_dispute_score_deposit", "min_creator_stake", "creator_application_fee", "dispute_score_reward", "min_task_training_in_days", "min_task_final_submission_in_days", "min_task_final_dispute_in_days", "trainers_reward_percentage", "scorer_reward_percentage", "stakers_reward_percentage", "trainer_first_place_reward_percentage", "trainer_second_place_reward_percentage", "trainer_third_place_reward_percentage", "trainers_number_to_be_rewarded_except_first_three")
    ADMIN_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_DURATION_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_REWARD_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_TRAINER_STAKE_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_SCORER_STAKE_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_COOLING_OFF_PERIOD_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MIN_REPORT_PLAGIARISM_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    MIN_DISPUTE_SCORE_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    MIN_CREATOR_STAKE_FIELD_NUMBER: _ClassVar[int]
    CREATOR_APPLICATION_FEE_FIELD_NUMBER: _ClassVar[int]
    DISPUTE_SCORE_REWARD_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_TRAINING_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_FINAL_SUBMISSION_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    MIN_TASK_FINAL_DISPUTE_IN_DAYS_FIELD_NUMBER: _ClassVar[int]
    TRAINERS_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    SCORER_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    STAKERS_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    TRAINER_FIRST_PLACE_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    TRAINER_SECOND_PLACE_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    TRAINER_THIRD_PLACE_REWARD_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    TRAINERS_NUMBER_TO_BE_REWARDED_EXCEPT_FIRST_THREE_FIELD_NUMBER: _ClassVar[int]
    admin_address: str
    min_task_duration_in_days: int
    min_task_reward: int
    min_task_trainer_stake: int
    min_task_scorer_stake: int
    submission_cooling_off_period_in_seconds: int
    min_report_plagiarism_deposit: int
    min_dispute_score_deposit: int
    min_creator_stake: int
    creator_application_fee: int
    dispute_score_reward: int
    min_task_training_in_days: int
    min_task_final_submission_in_days: int
    min_task_final_dispute_in_days: int
    trainers_reward_percentage: int
    scorer_reward_percentage: int
    stakers_reward_percentage: int
    trainer_first_place_reward_percentage: int
    trainer_second_place_reward_percentage: int
    trainer_third_place_reward_percentage: int
    trainers_number_to_be_rewarded_except_first_three: int
    def __init__(self, admin_address: _Optional[str] = ..., min_task_duration_in_days: _Optional[int] = ..., min_task_reward: _Optional[int] = ..., min_task_trainer_stake: _Optional[int] = ..., min_task_scorer_stake: _Optional[int] = ..., submission_cooling_off_period_in_seconds: _Optional[int] = ..., min_report_plagiarism_deposit: _Optional[int] = ..., min_dispute_score_deposit: _Optional[int] = ..., min_creator_stake: _Optional[int] = ..., creator_application_fee: _Optional[int] = ..., dispute_score_reward: _Optional[int] = ..., min_task_training_in_days: _Optional[int] = ..., min_task_final_submission_in_days: _Optional[int] = ..., min_task_final_dispute_in_days: _Optional[int] = ..., trainers_reward_percentage: _Optional[int] = ..., scorer_reward_percentage: _Optional[int] = ..., stakers_reward_percentage: _Optional[int] = ..., trainer_first_place_reward_percentage: _Optional[int] = ..., trainer_second_place_reward_percentage: _Optional[int] = ..., trainer_third_place_reward_percentage: _Optional[int] = ..., trainers_number_to_be_rewarded_except_first_three: _Optional[int] = ...) -> None: ...
