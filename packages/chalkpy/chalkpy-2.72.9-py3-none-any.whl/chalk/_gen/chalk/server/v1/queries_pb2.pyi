from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetQueryPerformanceSummaryRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class GetQueryPerformanceSummaryResponse(_message.Message):
    __slots__ = ("operation_id", "performance_summary")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    performance_summary: str
    def __init__(self, operation_id: _Optional[str] = ..., performance_summary: _Optional[str] = ...) -> None: ...
