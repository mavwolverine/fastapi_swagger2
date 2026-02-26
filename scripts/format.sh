#!/bin/sh -e
set -x

uv run ruff check src/fastapi_swagger2 tests scripts --fix --exclude tests/integration/petstore
uv run ruff format src/fastapi_swagger2 tests scripts --exclude tests/integration/petstore
