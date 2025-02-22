from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IdentityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IDENTITY_TYPE_UNKNOWN: _ClassVar[IdentityType]
    IDENTITY_TYPE_NONE: _ClassVar[IdentityType]
    IDENTITY_TYPE_SUB: _ClassVar[IdentityType]
    IDENTITY_TYPE_JWT: _ClassVar[IdentityType]
    IDENTITY_TYPE_MANUAL: _ClassVar[IdentityType]
IDENTITY_TYPE_UNKNOWN: IdentityType
IDENTITY_TYPE_NONE: IdentityType
IDENTITY_TYPE_SUB: IdentityType
IDENTITY_TYPE_JWT: IdentityType
IDENTITY_TYPE_MANUAL: IdentityType

class IdentityContext(_message.Message):
    __slots__ = ("identity", "type")
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    identity: str
    type: IdentityType
    def __init__(self, identity: _Optional[str] = ..., type: _Optional[_Union[IdentityType, str]] = ...) -> None: ...
