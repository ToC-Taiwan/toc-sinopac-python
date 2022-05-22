#!/bin/bash

python -m grpc_tools.protoc -I./protobuf --python_out=./src --mypy_out=./src --grpc_python_out=./src ./protobuf/*.proto
