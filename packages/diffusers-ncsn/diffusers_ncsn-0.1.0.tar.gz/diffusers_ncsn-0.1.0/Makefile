#
# Installation
#

.PHONY: setup
setup:
	pip install -U uv

.PHONY: install-training
install:
	uv sync --extra training

.PHONY: install-doc
install-doc:
	uv sync --extra doc

#
# linter/formatter/typecheck
#

.PHONY: lint
lint: install-training
	uv run ruff check --output-format=github .

.PHONY: format
format: install-training
	uv run ruff format --check --diff .

.PHONY: typecheck
typecheck: install
	uv run mypy --cache-dir=/dev/null .

.PHONY: test
test: install-training
	uv run pytest -vsx --log-cli-level=INFO

.PHONY: html
html: install-doc
	uv run sphinx-build -M html docs/source docs/build
