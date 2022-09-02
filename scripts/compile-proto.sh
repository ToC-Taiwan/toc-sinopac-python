#!/bin/bash

git clone git@gitlab.tocraw.com:root/toc-trade-protobuf.git

rm -rf pb

python -m grpc_tools.protoc \
    -I=./toc-trade-protobuf \
    --python_out=. \
    --mypy_out=. \
    --grpc_python_out=. \
    ./toc-trade-protobuf/pb/*.proto

rm -rf toc-trade-protobuf
