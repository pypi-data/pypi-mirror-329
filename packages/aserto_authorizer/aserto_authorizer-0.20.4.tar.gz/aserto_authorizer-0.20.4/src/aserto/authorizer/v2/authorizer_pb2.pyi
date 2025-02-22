from google.api import annotations_pb2 as _annotations_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from aserto.authorizer.v2.api import identity_context_pb2 as _identity_context_pb2
from aserto.authorizer.v2.api import policy_context_pb2 as _policy_context_pb2
from aserto.authorizer.v2.api import module_pb2 as _module_pb2
from aserto.authorizer.v2.api import policy_instance_pb2 as _policy_instance_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PathSeparator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PATH_SEPARATOR_UNKNOWN: _ClassVar[PathSeparator]
    PATH_SEPARATOR_DOT: _ClassVar[PathSeparator]
    PATH_SEPARATOR_SLASH: _ClassVar[PathSeparator]

class TraceLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRACE_LEVEL_UNKNOWN: _ClassVar[TraceLevel]
    TRACE_LEVEL_OFF: _ClassVar[TraceLevel]
    TRACE_LEVEL_FULL: _ClassVar[TraceLevel]
    TRACE_LEVEL_NOTES: _ClassVar[TraceLevel]
    TRACE_LEVEL_FAILS: _ClassVar[TraceLevel]
PATH_SEPARATOR_UNKNOWN: PathSeparator
PATH_SEPARATOR_DOT: PathSeparator
PATH_SEPARATOR_SLASH: PathSeparator
TRACE_LEVEL_UNKNOWN: TraceLevel
TRACE_LEVEL_OFF: TraceLevel
TRACE_LEVEL_FULL: TraceLevel
TRACE_LEVEL_NOTES: TraceLevel
TRACE_LEVEL_FAILS: TraceLevel

class InfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ("version", "commit", "date", "os", "arch")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    version: str
    commit: str
    date: str
    os: str
    arch: str
    def __init__(self, version: _Optional[str] = ..., commit: _Optional[str] = ..., date: _Optional[str] = ..., os: _Optional[str] = ..., arch: _Optional[str] = ...) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ("id", "field_mask", "policy_instance")
    ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    POLICY_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    field_mask: _field_mask_pb2.FieldMask
    policy_instance: _policy_instance_pb2.PolicyInstance
    def __init__(self, id: _Optional[str] = ..., field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., policy_instance: _Optional[_Union[_policy_instance_pb2.PolicyInstance, _Mapping]] = ...) -> None: ...

class GetPolicyResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _module_pb2.Module
    def __init__(self, result: _Optional[_Union[_module_pb2.Module, _Mapping]] = ...) -> None: ...

class ListPoliciesRequest(_message.Message):
    __slots__ = ("field_mask", "policy_instance")
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    POLICY_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    field_mask: _field_mask_pb2.FieldMask
    policy_instance: _policy_instance_pb2.PolicyInstance
    def __init__(self, field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., policy_instance: _Optional[_Union[_policy_instance_pb2.PolicyInstance, _Mapping]] = ...) -> None: ...

class ListPoliciesResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _containers.RepeatedCompositeFieldContainer[_module_pb2.Module]
    def __init__(self, result: _Optional[_Iterable[_Union[_module_pb2.Module, _Mapping]]] = ...) -> None: ...

class DecisionTreeRequest(_message.Message):
    __slots__ = ("policy_context", "identity_context", "options", "resource_context", "policy_instance")
    POLICY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    POLICY_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    policy_context: _policy_context_pb2.PolicyContext
    identity_context: _identity_context_pb2.IdentityContext
    options: DecisionTreeOptions
    resource_context: _struct_pb2.Struct
    policy_instance: _policy_instance_pb2.PolicyInstance
    def __init__(self, policy_context: _Optional[_Union[_policy_context_pb2.PolicyContext, _Mapping]] = ..., identity_context: _Optional[_Union[_identity_context_pb2.IdentityContext, _Mapping]] = ..., options: _Optional[_Union[DecisionTreeOptions, _Mapping]] = ..., resource_context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., policy_instance: _Optional[_Union[_policy_instance_pb2.PolicyInstance, _Mapping]] = ...) -> None: ...

class DecisionTreeOptions(_message.Message):
    __slots__ = ("path_separator",)
    PATH_SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    path_separator: PathSeparator
    def __init__(self, path_separator: _Optional[_Union[PathSeparator, str]] = ...) -> None: ...

class DecisionTreeResponse(_message.Message):
    __slots__ = ("path_root", "path")
    PATH_ROOT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    path_root: str
    path: _struct_pb2.Struct
    def __init__(self, path_root: _Optional[str] = ..., path: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class IsRequest(_message.Message):
    __slots__ = ("policy_context", "identity_context", "resource_context", "policy_instance")
    POLICY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    POLICY_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    policy_context: _policy_context_pb2.PolicyContext
    identity_context: _identity_context_pb2.IdentityContext
    resource_context: _struct_pb2.Struct
    policy_instance: _policy_instance_pb2.PolicyInstance
    def __init__(self, policy_context: _Optional[_Union[_policy_context_pb2.PolicyContext, _Mapping]] = ..., identity_context: _Optional[_Union[_identity_context_pb2.IdentityContext, _Mapping]] = ..., resource_context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., policy_instance: _Optional[_Union[_policy_instance_pb2.PolicyInstance, _Mapping]] = ...) -> None: ...

class Decision(_message.Message):
    __slots__ = ("decision",)
    DECISION_FIELD_NUMBER: _ClassVar[int]
    IS_FIELD_NUMBER: _ClassVar[int]
    decision: str
    def __init__(self, decision: _Optional[str] = ..., **kwargs) -> None: ...

class IsResponse(_message.Message):
    __slots__ = ("decisions",)
    DECISIONS_FIELD_NUMBER: _ClassVar[int]
    decisions: _containers.RepeatedCompositeFieldContainer[Decision]
    def __init__(self, decisions: _Optional[_Iterable[_Union[Decision, _Mapping]]] = ...) -> None: ...

class QueryOptions(_message.Message):
    __slots__ = ("metrics", "instrument", "trace", "trace_summary")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_FIELD_NUMBER: _ClassVar[int]
    TRACE_FIELD_NUMBER: _ClassVar[int]
    TRACE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    metrics: bool
    instrument: bool
    trace: TraceLevel
    trace_summary: bool
    def __init__(self, metrics: bool = ..., instrument: bool = ..., trace: _Optional[_Union[TraceLevel, str]] = ..., trace_summary: bool = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ("query", "input", "options", "policy_context", "identity_context", "resource_context", "policy_instance")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    POLICY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    POLICY_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    query: str
    input: str
    options: QueryOptions
    policy_context: _policy_context_pb2.PolicyContext
    identity_context: _identity_context_pb2.IdentityContext
    resource_context: _struct_pb2.Struct
    policy_instance: _policy_instance_pb2.PolicyInstance
    def __init__(self, query: _Optional[str] = ..., input: _Optional[str] = ..., options: _Optional[_Union[QueryOptions, _Mapping]] = ..., policy_context: _Optional[_Union[_policy_context_pb2.PolicyContext, _Mapping]] = ..., identity_context: _Optional[_Union[_identity_context_pb2.IdentityContext, _Mapping]] = ..., resource_context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., policy_instance: _Optional[_Union[_policy_instance_pb2.PolicyInstance, _Mapping]] = ...) -> None: ...

class CompileRequest(_message.Message):
    __slots__ = ("query", "input", "unknowns", "disable_inlining", "options", "policy_context", "identity_context", "resource_context", "policy_instance")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    UNKNOWNS_FIELD_NUMBER: _ClassVar[int]
    DISABLE_INLINING_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    POLICY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    POLICY_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    query: str
    input: str
    unknowns: _containers.RepeatedScalarFieldContainer[str]
    disable_inlining: _containers.RepeatedScalarFieldContainer[str]
    options: QueryOptions
    policy_context: _policy_context_pb2.PolicyContext
    identity_context: _identity_context_pb2.IdentityContext
    resource_context: _struct_pb2.Struct
    policy_instance: _policy_instance_pb2.PolicyInstance
    def __init__(self, query: _Optional[str] = ..., input: _Optional[str] = ..., unknowns: _Optional[_Iterable[str]] = ..., disable_inlining: _Optional[_Iterable[str]] = ..., options: _Optional[_Union[QueryOptions, _Mapping]] = ..., policy_context: _Optional[_Union[_policy_context_pb2.PolicyContext, _Mapping]] = ..., identity_context: _Optional[_Union[_identity_context_pb2.IdentityContext, _Mapping]] = ..., resource_context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., policy_instance: _Optional[_Union[_policy_instance_pb2.PolicyInstance, _Mapping]] = ...) -> None: ...

class CompileResponse(_message.Message):
    __slots__ = ("result", "metrics", "trace", "trace_summary")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    TRACE_FIELD_NUMBER: _ClassVar[int]
    TRACE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    result: _struct_pb2.Struct
    metrics: _struct_pb2.Struct
    trace: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    trace_summary: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, result: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., metrics: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., trace: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., trace_summary: _Optional[_Iterable[str]] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("response", "metrics", "trace", "trace_summary")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    TRACE_FIELD_NUMBER: _ClassVar[int]
    TRACE_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    response: _struct_pb2.Struct
    metrics: _struct_pb2.Struct
    trace: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    trace_summary: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, response: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., metrics: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., trace: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., trace_summary: _Optional[_Iterable[str]] = ...) -> None: ...
