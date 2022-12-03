#!/bin/bash

rm -rf toc-trade-protobuf
git clone git@github.com:ToC-Taiwan/toc-trade-protobuf.git

rm -rf pb
mkdir pb

python -m grpc_tools.protoc \
    -I=./toc-trade-protobuf \
    --python_out=./pb \
    --mypy_out=./pb \
    --grpc_python_out=./pb \
    ./toc-trade-protobuf/*.proto

rm ./pb/common_pb2_grpc.py
rm ./pb/app_pb2_grpc.py

git add ./pb

rm -rf toc-trade-protobuf
