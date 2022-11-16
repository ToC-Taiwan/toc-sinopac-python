#!/bin/bash

mypy --check-untyped-defs --config-file=./mypy.ini ./src > mypy_result
if grep error mypy_result
then
	exit 1
fi
exit 0
