#!/bin/bash

pylint ./src/ > pylint_result
if ! grep 10.00/10 pylint_result
then
	exit 1
fi

mypy --config-file=./mypy.ini ./src > mypy_result
if grep error mypy_result
then
	exit 1
fi

# git clean -fxd
exit 0
