#!/bin/sh -e
set -x

uv run ruff check src/fastapi_swagger2 tests scripts --fix
uv run black src/fastapi_swagger2 tests scripts
uv run isort src/fastapi_swagger2 tests scripts
