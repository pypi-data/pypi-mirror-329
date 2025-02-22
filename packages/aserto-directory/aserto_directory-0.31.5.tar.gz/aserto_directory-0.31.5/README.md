# Aserto Directory gRPC client
This is an automatically generated client for interacting with Aserto's
[Directory service](https://www.topaz.sh/docs/directory) using the gRPC protocol.

The code was generated from https://buf.build/aserto-dev/directory.

## Installation

### Using Pip
```sh
pip install aserto-directory
```

### Using Poetry
```sh
poetry add aserto-directory
```

## Usage
```py
import grpc
from aserto.directory.reader.v3 import ReaderStub, GetObjectRequest

with grpc.secure_channel(
    target="directory.prod.aserto.com:8443",
    credentials=grpc.ssl_channel_credentials(),
) as channel:
    reader = ReaderStub(channel)

    # Read an object from the directory.
    response = reader.GetObject(
        GetObjectRequest(object_type="user", object_id="rick@the-citadel.com"),
        metadata=(
            ("authorization", f"basic {ASERTO_DIRECTORY_API_KEY}"),
            ("aserto-tenant-id", ASERTO_TENANT_ID),
        ),
    )

    print("Object:", object_type.result)
