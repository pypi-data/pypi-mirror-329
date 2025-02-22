# Aserto Authorizer gRPC client
This is an automatically generated client for interacting with Aserto's [Authorizer service](https://docs.aserto.com/docs/authorizer-guide/overview) using the gRPC protocol.

The code was generated from https://buf.build/aserto-dev/authorizer.


## Installation

### Using Pip
```sh
pip install aserto-authorizer
```

### Using Poetry
```sh
poetry add aserto-authorizer
```

## Usage

```py
import grpc
from aserto.authorizer.v2.api import (
    IdentityContext,
    IdentityType,
    PolicyContext,
    PolicyInstance,
)
from aserto.authorizer.v2 import (
    AuthorizerStub,
    DecisionTreeRequest,
    DecisionTreeOptions,
    DecisionTreeResponse,
    PathSeparator,
)
from grpclib.client import Channel


with grpc.secure_channel(
    target="authorizer.prod.aserto.com:8443",
    credentials=grpc.ssl_channel_credentials(),
) as channel:
    client = AuthorizerStub(channel)

    response = client.DecisionTree(
        DecisionTreeRequest(
            policy_context=PolicyContext(
                path=ASERTO_POLICY_PATH_ROOT,
                decisions=["visible", "enabled", "allowed"],
            ),
            policy_instance=PolicyInstance(
                name=ASERTO_POLICY_NAME,
                instance_label=ASERTO_POLICY_INSTANCE_LABEL,
            ),
            identity_context=IdentityContext(type=IdentityType.IDENTITY_TYPE_NONE),
            options=DecisionTreeOptions(
                path_separator=PathSeparator.PATH_SEPARATOR_DOT,
            ),
        )
    )

    assert response == DecisionTreeResponse(
        path_root=ASERTO_POLICY_PATH_ROOT,
        path=Proto.Struct(
            fields={
                "GET.your.policy.path": Proto.Value(
                    struct_value=Proto.Struct(
                        fields={
                            "visible": Proto.Value(bool_value=True),
                            "enabled": Proto.Value(bool_value=True),
                            "allowed": Proto.Value(bool_value=False),
                        },
                    ),
                ),
            },
        ),
    )
```
