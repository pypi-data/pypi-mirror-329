# Python Client for Viu API

This package provides the generated Python client code for accessing various text embedding services
via gRPC. It is built from proto files found in the `proto` directory.

## Installation

Install the package using pip:

```bash
pip install python-viu-api
```

## Usage

Import the generated modules in your Python code:

```python
from python_viu_api import jinaembed_pb2, viu_api_pb2, viu_api_pb2_grpc
import grpc

# Example: Create a request for Jina embeddings
request = jinaembed_pb2.JinaEmbedRequest(
    texts=["Sample text"],
    task=jinaembed_pb2.RETRIEVAL_QUERY,
    truncate_dim=128
)

# Set up a gRPC channel (adjust the target as needed)
channel = grpc.insecure_channel('localhost:50051')
stub = viu_api_pb2_grpc.ApiServiceStub(channel)

# Call the EmbedJinaEmbeddingsV3 RPC
response = stub.EmbedJinaEmbeddingsV3(request)
print(response)
```

## Supported Models

- NVEmbedV2
- BGEGemma2
- JinaEmbeddingsV3

