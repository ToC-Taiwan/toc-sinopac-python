#!/bin/bash

mypy --config-file=./mypy.ini ./src && pylint ./src
