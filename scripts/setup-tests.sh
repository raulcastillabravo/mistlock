#!/bin/bash
# This script prepares the local environment for running MVE tests.
# It MUST be executed before running tests for the first time.
set -e

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Install Python
uv python install 3.12
uv python pin 3.12

# Create .venv
uv sync

# Install Dev Containers CLI an add a link for pytest to use it
curl -fsSL https://raw.githubusercontent.com/devcontainers/cli/main/scripts/install.sh | sh
ln -sf "$HOME/.devcontainers/bin/devcontainer" "./.venv/bin/devcontainer"

echo -e "\nSetup completed successfully!"

