ARCH=$(shell uname -m)
PYTHON=$(shell which python3)
PIP=$(shell which pip3)
PWD=$(shell pwd)
PBPATH=$(PWD)/src/pb

run: check ### run
	@SJ_LOG_PATH=$(PWD)/logs/shioaji.log SJ_CONTRACTS_PATH=$(PWD)/data PYTHONPATH=$(PBPATH) $(PYTHON) -BOO ./src/main.py
.PHONY: run

lint: check ### lint
	@mypy --check-untyped-defs --config-file=./mypy.ini ./src
	@PYTHONPATH=$(PBPATH) PYLINTHOME=$(PWD) pylint ./src
.PHONY: lint

install: check ### install dependencies
	@$(PIP) install --no-warn-script-location --no-cache-dir -r requirements.txt
	@$(PIP) install --no-warn-script-location --no-cache-dir mypy-protobuf pylint-protobuf mypy pylint
	@mypy --install-types --check-untyped-defs --non-interactive ./src
.PHONY: install

update: check ### update dependencies
	@./scripts/update_dependency.sh $(PIP)
	@./scripts/install_dev_dependency.sh $(PIP)
	@./scripts/compile-proto.sh $(PYTHON)
.PHONY: update

proto: check ### compile proto
	@./scripts/compile-proto.sh $(PYTHON)
.PHONY: proto

check: ## check environment
ifneq ($(PYTHON),$(PWD)/venv/bin/python3)
	$(error "Please run 'make venv' first")
endif
	@echo "Venv python version: $(shell $(PYTHON) --version | awk '{print $$2}')"
	@echo "Python path: $(PYTHON)"
.PHONY: check

venv: clean ## create virtual environment
ifneq ($(ARCH),x86_64)
	$(error "This script only supports x86_64")
endif
	@$(PYTHON) -m venv venv
.PHONY: venv

clean: ## clear virtual environment
	@rm -rf venv
.PHONY: clean

help: ## display this help screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help
