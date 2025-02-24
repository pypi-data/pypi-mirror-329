from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ErrorCode_NOERROR: _ClassVar[ErrorCode]
    ErrorCode_INVALID_ADDRESS: _ClassVar[ErrorCode]
    ErrorCode_INVALID_TASK_STATUS: _ClassVar[ErrorCode]
    ErrorCode_NOT_PROPOSER: _ClassVar[ErrorCode]
    ErrorCode_NOT_VALIDATOR: _ClassVar[ErrorCode]
    ErrorCode_ALREADY_ASSIGNED: _ClassVar[ErrorCode]
    ErrorCode_STAKE_NOT_ENOUGH: _ClassVar[ErrorCode]
    ErrorCode_ALREADY_SUBMITTED: _ClassVar[ErrorCode]
    ErrorCode_NOT_AUTHORIZED: _ClassVar[ErrorCode]
    ErrorCode_MIN_TIME_NOT_PASSED: _ClassVar[ErrorCode]
    ErrorCode_COLLECTION_ERROR: _ClassVar[ErrorCode]
    ErrorCode_BLACKLISTED: _ClassVar[ErrorCode]
    ErrorCode_ALREADY_VALIDATOR: _ClassVar[ErrorCode]
    ErrorCode_ALREADY_PROPOSER: _ClassVar[ErrorCode]
    ErrorCode_WRONG_ROUND: _ClassVar[ErrorCode]
    ErrorCode_PENDING_DISPUTE: _ClassVar[ErrorCode]
ErrorCode_NOERROR: ErrorCode
ErrorCode_INVALID_ADDRESS: ErrorCode
ErrorCode_INVALID_TASK_STATUS: ErrorCode
ErrorCode_NOT_PROPOSER: ErrorCode
ErrorCode_NOT_VALIDATOR: ErrorCode
ErrorCode_ALREADY_ASSIGNED: ErrorCode
ErrorCode_STAKE_NOT_ENOUGH: ErrorCode
ErrorCode_ALREADY_SUBMITTED: ErrorCode
ErrorCode_NOT_AUTHORIZED: ErrorCode
ErrorCode_MIN_TIME_NOT_PASSED: ErrorCode
ErrorCode_COLLECTION_ERROR: ErrorCode
ErrorCode_BLACKLISTED: ErrorCode
ErrorCode_ALREADY_VALIDATOR: ErrorCode
ErrorCode_ALREADY_PROPOSER: ErrorCode
ErrorCode_WRONG_ROUND: ErrorCode
ErrorCode_PENDING_DISPUTE: ErrorCode
