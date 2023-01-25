PIP=$(shell which pip3)
PYTHON=$(shell which python3)
PBPATH=$(PWD)/src/pb

run: ### run
	@clear && PYTHONPATH=$(PBPATH) $(PYTHON) -BOO ./src/main.py
.PHONY: run

lint: ### lint
	@mypy --check-untyped-defs --config-file=./mypy.ini ./src
	@PYTHONPATH=$(PBPATH) PYLINTHOME=$(PWD) pylint ./src
.PHONY: lint

install: ### install dependencies
	@$(PIP) install --no-warn-script-location --no-cache-dir -r requirements.txt
	@$(PIP) install --no-warn-script-location --no-cache-dir mypy-protobuf pylint-protobuf mypy pylint
	@mypy --install-types --check-untyped-defs --non-interactive ./src
.PHONY: install

update: ### update dependencies
	@./scripts/update_dependency.sh $(PIP)
	@./scripts/install_dev_dependency.sh $(PIP)
	@./scripts/compile-proto.sh $(PYTHON)
.PHONY: update

proto: ### compile proto
	@./scripts/compile-proto.sh $(PYTHON)
.PHONY: proto

help: ## display this help screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help
