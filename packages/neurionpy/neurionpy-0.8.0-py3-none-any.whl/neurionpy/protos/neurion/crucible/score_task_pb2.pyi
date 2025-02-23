from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScoreTask(_message.Message):
    __slots__ = ("id", "task_id", "submission_id", "result_to_check", "metainfo", "scorer", "created_timestamp", "score", "score_timestamp", "task_kit")
    ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_TO_CHECK_FIELD_NUMBER: _ClassVar[int]
    METAINFO_FIELD_NUMBER: _ClassVar[int]
    SCORER_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    SCORE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TASK_KIT_FIELD_NUMBER: _ClassVar[int]
    id: int
    task_id: int
    submission_id: int
    result_to_check: str
    metainfo: str
    scorer: str
    created_timestamp: int
    score: str
    score_timestamp: int
    task_kit: str
    def __init__(self, id: _Optional[int] = ..., task_id: _Optional[int] = ..., submission_id: _Optional[int] = ..., result_to_check: _Optional[str] = ..., metainfo: _Optional[str] = ..., scorer: _Optional[str] = ..., created_timestamp: _Optional[int] = ..., score: _Optional[str] = ..., score_timestamp: _Optional[int] = ..., task_kit: _Optional[str] = ...) -> None: ...
