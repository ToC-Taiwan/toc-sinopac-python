include .env
export

run: ### run
	@python -BOO ./src/main.py
.PHONY: run

help: ## display this help screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help

lint: ### lint
	@mypy --check-untyped-defs --config-file=./mypy.ini ./src && pylint ./src
.PHONY: lint

update: ### update dependencies
	@./scripts/update_dependency.sh && ./scripts/install_dev_dependency.sh && ./scripts/compile-proto.sh
.PHONY: update
