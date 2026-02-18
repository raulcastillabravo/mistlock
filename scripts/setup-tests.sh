#!/bin/bash
# This script prepares the local environment for running MVE tests.
# It MUST be executed before running tests for the first time.
set -e

# 1. Install uv if not present
command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Setup Python environment
uv python install 3.12
uv python pin 3.12
uv sync

# 3. Install Dev Containers CLI if not present
command -v devcontainer >/dev/null 2>&1 || curl -fsSL https://raw.githubusercontent.com/devcontainers/cli/main/scripts/install.sh | sh

# 4. Link CLI for pytest
DEVCONTAINER_BIN=$(command -v devcontainer || echo "$HOME/.devcontainers/bin/devcontainer")
ln -sf "$DEVCONTAINER_BIN" "./.venv/bin/devcontainer"

echo -e "\nSetup completed successfully!"

