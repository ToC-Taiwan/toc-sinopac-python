#!/bin/sh

if [ -d "lib" ]; then
    rm -rf lib
fi

if [ -d "bin" ]; then
    rm -rf bin
fi

if [ -f "pyvenv.cfg" ]; then
    rm -rf pyvenv.cfg
fi

python3 -m venv ./
source ./bin/activate
