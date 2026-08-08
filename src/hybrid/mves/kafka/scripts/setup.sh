#!/bin/bash
set -e

command -v mise >/dev/null 2>&1 || (curl https://mise.run | sh)
export PATH="$HOME/.local/bin:$PATH"

mise install -y
mise run setup

echo "✓ Environment setup complete"
