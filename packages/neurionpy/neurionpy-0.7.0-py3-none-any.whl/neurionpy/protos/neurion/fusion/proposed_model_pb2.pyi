from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ProposedModel(_message.Message):
    __slots__ = ("id", "creator", "task_id", "round", "model", "metainfo", "created_timestamp", "score", "validator", "scored", "scored_timestamp", "is_disputed", "dispute_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    METAINFO_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_FIELD_NUMBER: _ClassVar[int]
    SCORED_FIELD_NUMBER: _ClassVar[int]
    SCORED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    IS_DISPUTED_FIELD_NUMBER: _ClassVar[int]
    DISPUTE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    task_id: int
    round: int
    model: str
    metainfo: str
    created_timestamp: int
    score: str
    validator: str
    scored: bool
    scored_timestamp: int
    is_disputed: bool
    dispute_id: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., task_id: _Optional[int] = ..., round: _Optional[int] = ..., model: _Optional[str] = ..., metainfo: _Optional[str] = ..., created_timestamp: _Optional[int] = ..., score: _Optional[str] = ..., validator: _Optional[str] = ..., scored: bool = ..., scored_timestamp: _Optional[int] = ..., is_disputed: bool = ..., dispute_id: _Optional[int] = ...) -> None: ...
