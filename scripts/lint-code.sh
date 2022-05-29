#!/bin/bash

mypy --install-types --non-interactive ./src && pylint ./src
