from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlagiarismReportResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLAGIARISM_REPORT_RESULT_NOT_AVAILABLE: _ClassVar[PlagiarismReportResult]
    PLAGIARISM_REPORT_RESULT_ACCEPTED: _ClassVar[PlagiarismReportResult]
    PLAGIARISM_REPORT_RESULT_REJECTED: _ClassVar[PlagiarismReportResult]
PLAGIARISM_REPORT_RESULT_NOT_AVAILABLE: PlagiarismReportResult
PLAGIARISM_REPORT_RESULT_ACCEPTED: PlagiarismReportResult
PLAGIARISM_REPORT_RESULT_REJECTED: PlagiarismReportResult

class PlagiarismReport(_message.Message):
    __slots__ = ("id", "task_id", "copied_submission_id", "suspected_submission_id", "arbitrator", "result", "created_timestamp", "decision_timestamp", "proof_of_plagiarism", "reason_for_rejection", "deposit", "reporter", "reportee")
    ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    COPIED_SUBMISSION_ID_FIELD_NUMBER: _ClassVar[int]
    SUSPECTED_SUBMISSION_ID_FIELD_NUMBER: _ClassVar[int]
    ARBITRATOR_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DECISION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PROOF_OF_PLAGIARISM_FIELD_NUMBER: _ClassVar[int]
    REASON_FOR_REJECTION_FIELD_NUMBER: _ClassVar[int]
    DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    REPORTER_FIELD_NUMBER: _ClassVar[int]
    REPORTEE_FIELD_NUMBER: _ClassVar[int]
    id: int
    task_id: int
    copied_submission_id: int
    suspected_submission_id: int
    arbitrator: str
    result: PlagiarismReportResult
    created_timestamp: int
    decision_timestamp: int
    proof_of_plagiarism: str
    reason_for_rejection: str
    deposit: int
    reporter: str
    reportee: str
    def __init__(self, id: _Optional[int] = ..., task_id: _Optional[int] = ..., copied_submission_id: _Optional[int] = ..., suspected_submission_id: _Optional[int] = ..., arbitrator: _Optional[str] = ..., result: _Optional[_Union[PlagiarismReportResult, str]] = ..., created_timestamp: _Optional[int] = ..., decision_timestamp: _Optional[int] = ..., proof_of_plagiarism: _Optional[str] = ..., reason_for_rejection: _Optional[str] = ..., deposit: _Optional[int] = ..., reporter: _Optional[str] = ..., reportee: _Optional[str] = ...) -> None: ...
