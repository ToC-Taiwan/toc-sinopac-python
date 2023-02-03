#!/bin/sh

rm -rf lib
rm -rf bin
rm -rf pyvenv.cfg

python3 -m venv ./
source ./bin/activate
