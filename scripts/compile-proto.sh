#!/bin/sh

if [ $# -eq 0 ]; then
  echo "No python supplied"
  exit 1
fi

python=$1

rm -rf toc-trade-protobuf
git clone git@github.com:ToC-Taiwan/toc-trade-protobuf.git

outpath=./src/pb
rm -rf $outpath
mkdir $outpath

$python -m grpc_tools.protoc \
  --python_out=$outpath \
  --grpc_python_out=$outpath \
  --mypy_out=$outpath \
  --proto_path=./toc-trade-protobuf/protos/v3 \
  ./toc-trade-protobuf/protos/v3/*/*.proto

rm $outpath/app/app_pb2_grpc.py
rm $outpath/forwarder/entity_pb2_grpc.py
rm $outpath/forwarder/mq_pb2_grpc.py

git add $outpath

rm -rf toc-trade-protobuf
