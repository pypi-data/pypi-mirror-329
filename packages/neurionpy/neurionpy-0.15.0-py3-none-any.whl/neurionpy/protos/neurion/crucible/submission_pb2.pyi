from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Submission(_message.Message):
    __slots__ = ("id", "creator", "task_id", "result", "metainfo", "created_timestamp", "score", "scorer", "scored", "scored_timestamp", "encrypted_proof_of_ownership", "revealed_proof_of_ownership", "is_final", "is_disputed", "dispute_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    METAINFO_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    SCORER_FIELD_NUMBER: _ClassVar[int]
    SCORED_FIELD_NUMBER: _ClassVar[int]
    SCORED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_PROOF_OF_OWNERSHIP_FIELD_NUMBER: _ClassVar[int]
    REVEALED_PROOF_OF_OWNERSHIP_FIELD_NUMBER: _ClassVar[int]
    IS_FINAL_FIELD_NUMBER: _ClassVar[int]
    IS_DISPUTED_FIELD_NUMBER: _ClassVar[int]
    DISPUTE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator: str
    task_id: int
    result: str
    metainfo: str
    created_timestamp: int
    score: str
    scorer: str
    scored: bool
    scored_timestamp: int
    encrypted_proof_of_ownership: str
    revealed_proof_of_ownership: str
    is_final: bool
    is_disputed: bool
    dispute_id: int
    def __init__(self, id: _Optional[int] = ..., creator: _Optional[str] = ..., task_id: _Optional[int] = ..., result: _Optional[str] = ..., metainfo: _Optional[str] = ..., created_timestamp: _Optional[int] = ..., score: _Optional[str] = ..., scorer: _Optional[str] = ..., scored: bool = ..., scored_timestamp: _Optional[int] = ..., encrypted_proof_of_ownership: _Optional[str] = ..., revealed_proof_of_ownership: _Optional[str] = ..., is_final: bool = ..., is_disputed: bool = ..., dispute_id: _Optional[int] = ...) -> None: ...
