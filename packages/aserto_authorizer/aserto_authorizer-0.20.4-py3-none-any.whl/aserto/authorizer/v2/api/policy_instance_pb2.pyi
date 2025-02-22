from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyInstance(_message.Message):
    __slots__ = ("name", "instance_label")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_LABEL_FIELD_NUMBER: _ClassVar[int]
    name: str
    instance_label: str
    def __init__(self, name: _Optional[str] = ..., instance_label: _Optional[str] = ...) -> None: ...
