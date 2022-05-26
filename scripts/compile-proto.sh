#!/bin/bash

git clone git@gitlab.tocraw.com:root/toc-trade-protobuf.git

python -m grpc_tools.protoc \
    -I=./toc-trade-protobuf/src \
    --python_out=./src \
    --mypy_out=./src \
    --grpc_python_out=./src \
    ./toc-trade-protobuf/src/*.proto

rm -rf toc-trade-protobuf

git add ./src/sinopac_forwarder_pb2_grpc.py
git add ./src/sinopac_forwarder_pb2.py
git add ./src/sinopac_forwarder_pb2.pyi
