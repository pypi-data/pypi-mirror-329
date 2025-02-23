from cometbft.types.v1 import types_pb2 as _types_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RemoteSignerError(_message.Message):
    __slots__ = ("code", "description")
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    code: int
    description: str
    def __init__(self, code: _Optional[int] = ..., description: _Optional[str] = ...) -> None: ...

class PubKeyRequest(_message.Message):
    __slots__ = ("chain_id",)
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    chain_id: str
    def __init__(self, chain_id: _Optional[str] = ...) -> None: ...

class PubKeyResponse(_message.Message):
    __slots__ = ("error", "pub_key_bytes", "pub_key_type")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_BYTES_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    error: RemoteSignerError
    pub_key_bytes: bytes
    pub_key_type: str
    def __init__(self, error: _Optional[_Union[RemoteSignerError, _Mapping]] = ..., pub_key_bytes: _Optional[bytes] = ..., pub_key_type: _Optional[str] = ...) -> None: ...

class SignVoteRequest(_message.Message):
    __slots__ = ("vote", "chain_id", "skip_extension_signing")
    VOTE_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    SKIP_EXTENSION_SIGNING_FIELD_NUMBER: _ClassVar[int]
    vote: _types_pb2.Vote
    chain_id: str
    skip_extension_signing: bool
    def __init__(self, vote: _Optional[_Union[_types_pb2.Vote, _Mapping]] = ..., chain_id: _Optional[str] = ..., skip_extension_signing: bool = ...) -> None: ...

class SignedVoteResponse(_message.Message):
    __slots__ = ("vote", "error")
    VOTE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    vote: _types_pb2.Vote
    error: RemoteSignerError
    def __init__(self, vote: _Optional[_Union[_types_pb2.Vote, _Mapping]] = ..., error: _Optional[_Union[RemoteSignerError, _Mapping]] = ...) -> None: ...

class SignProposalRequest(_message.Message):
    __slots__ = ("proposal", "chain_id")
    PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    proposal: _types_pb2.Proposal
    chain_id: str
    def __init__(self, proposal: _Optional[_Union[_types_pb2.Proposal, _Mapping]] = ..., chain_id: _Optional[str] = ...) -> None: ...

class SignedProposalResponse(_message.Message):
    __slots__ = ("proposal", "error")
    PROPOSAL_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    proposal: _types_pb2.Proposal
    error: RemoteSignerError
    def __init__(self, proposal: _Optional[_Union[_types_pb2.Proposal, _Mapping]] = ..., error: _Optional[_Union[RemoteSignerError, _Mapping]] = ...) -> None: ...

class SignBytesRequest(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    def __init__(self, value: _Optional[bytes] = ...) -> None: ...

class SignBytesResponse(_message.Message):
    __slots__ = ("signature", "error")
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    signature: bytes
    error: RemoteSignerError
    def __init__(self, signature: _Optional[bytes] = ..., error: _Optional[_Union[RemoteSignerError, _Mapping]] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Message(_message.Message):
    __slots__ = ("pub_key_request", "pub_key_response", "sign_vote_request", "signed_vote_response", "sign_proposal_request", "signed_proposal_response", "ping_request", "ping_response", "sign_bytes_request", "sign_bytes_response")
    PUB_KEY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGN_VOTE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SIGNED_VOTE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGN_PROPOSAL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SIGNED_PROPOSAL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PING_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PING_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGN_BYTES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SIGN_BYTES_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    pub_key_request: PubKeyRequest
    pub_key_response: PubKeyResponse
    sign_vote_request: SignVoteRequest
    signed_vote_response: SignedVoteResponse
    sign_proposal_request: SignProposalRequest
    signed_proposal_response: SignedProposalResponse
    ping_request: PingRequest
    ping_response: PingResponse
    sign_bytes_request: SignBytesRequest
    sign_bytes_response: SignBytesResponse
    def __init__(self, pub_key_request: _Optional[_Union[PubKeyRequest, _Mapping]] = ..., pub_key_response: _Optional[_Union[PubKeyResponse, _Mapping]] = ..., sign_vote_request: _Optional[_Union[SignVoteRequest, _Mapping]] = ..., signed_vote_response: _Optional[_Union[SignedVoteResponse, _Mapping]] = ..., sign_proposal_request: _Optional[_Union[SignProposalRequest, _Mapping]] = ..., signed_proposal_response: _Optional[_Union[SignedProposalResponse, _Mapping]] = ..., ping_request: _Optional[_Union[PingRequest, _Mapping]] = ..., ping_response: _Optional[_Union[PingResponse, _Mapping]] = ..., sign_bytes_request: _Optional[_Union[SignBytesRequest, _Mapping]] = ..., sign_bytes_response: _Optional[_Union[SignBytesResponse, _Mapping]] = ...) -> None: ...
