#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "No pip supplied"
    exit 1
fi

pip=$1

$pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  mypy-protobuf \
  pylint-protobuf \
  black \
  mypy \
  pylint

mypy --install-types --non-interactive --check-untyped-defs --config-file=./mypy.ini ./src

pre-commit autoupdate
pre-commit install
pre-commit run --all-files
