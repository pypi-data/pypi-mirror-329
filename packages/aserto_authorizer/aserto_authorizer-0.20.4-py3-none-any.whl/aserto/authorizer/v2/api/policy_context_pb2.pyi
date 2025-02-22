from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyContext(_message.Message):
    __slots__ = ("path", "decisions")
    PATH_FIELD_NUMBER: _ClassVar[int]
    DECISIONS_FIELD_NUMBER: _ClassVar[int]
    path: str
    decisions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, path: _Optional[str] = ..., decisions: _Optional[_Iterable[str]] = ...) -> None: ...
