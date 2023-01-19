#!/bin/sh

python=$1

rm -rf toc-trade-protobuf
git clone git@github.com:ToC-Taiwan/toc-trade-protobuf.git

outpath=./src/pb
rm -rf $outpath
mkdir $outpath

python3 -m grpc_tools.protoc \
    --python_out=$outpath \
    --pyi_out=$outpath \
    --grpc_python_out=$outpath \
    --proto_path=./toc-trade-protobuf/protos/v3/app \
    --proto_path=./toc-trade-protobuf/protos/v3/basic \
    --proto_path=./toc-trade-protobuf/protos/v3/common \
    --proto_path=./toc-trade-protobuf/protos/v3/health \
    --proto_path=./toc-trade-protobuf/protos/v3/history \
    --proto_path=./toc-trade-protobuf/protos/v3/stream \
    --proto_path=./toc-trade-protobuf/protos/v3/trade \
    ./toc-trade-protobuf/protos/v3/*/*.proto

rm $outpath/common_pb2_grpc.py
rm $outpath/app_pb2_grpc.py

git add $outpath

rm -rf toc-trade-protobuf
