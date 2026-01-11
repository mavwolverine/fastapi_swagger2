#!/usr/bin/env bash

set -e
set -x

uv run mypy src/fastapi_swagger2
uv run ruff check src/fastapi_swagger2 tests scripts
uv run black src/fastapi_swagger2 tests --check
uv run isort src/fastapi_swagger2 tests scripts --check-only
