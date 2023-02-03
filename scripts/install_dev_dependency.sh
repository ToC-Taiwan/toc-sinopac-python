#!/bin/sh

pip=$1

$pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  pre-commit \
  mypy-protobuf \
  pylint-protobuf \
  black \
  mypy \
  pylint

mypy --install-types --non-interactive --check-untyped-defs --config-file=./mypy.ini ./src

pre-commit autoupdate
pre-commit install
pre-commit run --all-files
