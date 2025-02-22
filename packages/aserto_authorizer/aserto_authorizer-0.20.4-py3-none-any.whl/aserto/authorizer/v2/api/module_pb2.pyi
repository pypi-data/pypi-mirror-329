from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Module(_message.Message):
    __slots__ = ("id", "raw", "package_path", "ast", "package_root")
    ID_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    AST_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_ROOT_FIELD_NUMBER: _ClassVar[int]
    id: str
    raw: str
    package_path: str
    ast: _struct_pb2.Value
    package_root: str
    def __init__(self, id: _Optional[str] = ..., raw: _Optional[str] = ..., package_path: _Optional[str] = ..., ast: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ..., package_root: _Optional[str] = ...) -> None: ...
