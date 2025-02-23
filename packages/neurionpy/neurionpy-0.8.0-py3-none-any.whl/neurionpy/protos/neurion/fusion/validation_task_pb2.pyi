from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ValidationTask(_message.Message):
    __slots__ = ("id", "task_id", "proposed_model_id", "model", "metainfo", "validator", "created_timestamp", "score", "score_timestamp", "testset", "round")
    ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    PROPOSED_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    METAINFO_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    SCORE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TESTSET_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    id: int
    task_id: int
    proposed_model_id: int
    model: str
    metainfo: str
    validator: str
    created_timestamp: int
    score: str
    score_timestamp: int
    testset: str
    round: int
    def __init__(self, id: _Optional[int] = ..., task_id: _Optional[int] = ..., proposed_model_id: _Optional[int] = ..., model: _Optional[str] = ..., metainfo: _Optional[str] = ..., validator: _Optional[str] = ..., created_timestamp: _Optional[int] = ..., score: _Optional[str] = ..., score_timestamp: _Optional[int] = ..., testset: _Optional[str] = ..., round: _Optional[int] = ...) -> None: ...
