#!/usr/bin/env bash

set -e
set -x

uv run mypy src/fastapi_swagger2
uv run ruff check src/fastapi_swagger2 tests scripts
uv run ruff format src/fastapi_swagger2 tests scripts --check
