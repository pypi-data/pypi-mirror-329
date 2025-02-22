from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from aserto.authorizer.v2.api import policy_context_pb2 as _policy_context_pb2
from aserto.authorizer.v2.api import identity_context_pb2 as _identity_context_pb2
from aserto.authorizer.v2.api import policy_instance_pb2 as _policy_instance_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Decision(_message.Message):
    __slots__ = ("id", "timestamp", "path", "user", "policy", "outcomes", "resource", "annotations", "tenant_id")
    class OutcomesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...
    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    timestamp: _timestamp_pb2.Timestamp
    path: str
    user: DecisionUser
    policy: DecisionPolicy
    outcomes: _containers.ScalarMap[str, bool]
    resource: _struct_pb2.Struct
    annotations: _containers.ScalarMap[str, str]
    tenant_id: str
    def __init__(self, id: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., path: _Optional[str] = ..., user: _Optional[_Union[DecisionUser, _Mapping]] = ..., policy: _Optional[_Union[DecisionPolicy, _Mapping]] = ..., outcomes: _Optional[_Mapping[str, bool]] = ..., resource: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., annotations: _Optional[_Mapping[str, str]] = ..., tenant_id: _Optional[str] = ...) -> None: ...

class DecisionUser(_message.Message):
    __slots__ = ("context", "id", "email")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    context: _identity_context_pb2.IdentityContext
    id: str
    email: str
    def __init__(self, context: _Optional[_Union[_identity_context_pb2.IdentityContext, _Mapping]] = ..., id: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class DecisionPolicy(_message.Message):
    __slots__ = ("context", "registry_service", "registry_image", "registry_tag", "registry_digest", "policy_instance")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_SERVICE_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_IMAGE_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_TAG_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_DIGEST_FIELD_NUMBER: _ClassVar[int]
    POLICY_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    context: _policy_context_pb2.PolicyContext
    registry_service: str
    registry_image: str
    registry_tag: str
    registry_digest: str
    policy_instance: _policy_instance_pb2.PolicyInstance
    def __init__(self, context: _Optional[_Union[_policy_context_pb2.PolicyContext, _Mapping]] = ..., registry_service: _Optional[str] = ..., registry_image: _Optional[str] = ..., registry_tag: _Optional[str] = ..., registry_digest: _Optional[str] = ..., policy_instance: _Optional[_Union[_policy_instance_pb2.PolicyInstance, _Mapping]] = ...) -> None: ...
