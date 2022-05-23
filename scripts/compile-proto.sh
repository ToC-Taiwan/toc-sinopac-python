#!/bin/bash

git clone git@gitlab.tocraw.com:root/toc-trade-protobuf.git
python -m grpc_tools.protoc -I./protobuf --python_out=./src --mypy_out=./src --grpc_python_out=./src ./protobuf/*.proto
rm -rf toc-trade-protobuf
