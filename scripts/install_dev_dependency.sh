#!/bin/bash

pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  pre-commit \
  mypy-protobuf \
  pylint-protobuf \
  black \
  mypy \
  pylint

mypy --install-types --non-interactive ./src
pre-commit install
