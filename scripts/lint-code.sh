#!/bin/bash

mypy --check-untyped-defs --config-file=./mypy.ini ./src && pylint ./src
