#!/bin/bash
set -e

# Install mise
(curl https://mise.run | sh)
export PATH="$HOME/.local/bin:$PATH"

# Run mise tasks
mise install -y
uv sync

# Install Azure Functions Core Tools if not present
if ! command -v func &> /dev/null; then
    echo "Installing Azure Functions Core Tools..."
    npm install -g azure-functions-core-tools@4 --unsafe-perm true
fi
