#!/usr/bin/env bash

# Nox Test Runner
# ================
# Runs tests across multiple Python and FastAPI versions using nox.
#
# Usage:
#   ./scripts/test-nox.sh                                    # Run all test sessions
#   ./scripts/test-nox.sh -s test-3.12                       # Run specific Python version (all FastAPI versions)
#   ./scripts/test-nox.sh -s test-3.12-fastapi_version-latest # Run specific Python + FastAPI version
#   ./scripts/test-nox.sh -s test-3.12-fastapi_version-0.128.0
#   ./scripts/test-nox.sh -l                                 # List all available sessions
#
# Requirements:
#   - nox must be installed: uv sync --group dev
#   - Submodule must be initialized: git submodule update --init --recursive

set -e
set -x

# Clean cached "latest" sessions to ensure fresh FastAPI version
rm -rf .nox/*-latest

nox "$@"
