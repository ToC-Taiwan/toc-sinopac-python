#!/bin/bash

pylint ./src/ > pylint_result
if ! grep 10.00/10 pylint_result
then
	exit 1
fi
exit 0
