#!/bin/bash
set -e

# Run all tests using the virtual environment
.venv/bin/python -m pytest tests/
