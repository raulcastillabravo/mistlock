#!/bin/bash
set -e

pip3 install uv
uv venv --clear --python python3
uv sync

echo "✓ Environment setup complete"
