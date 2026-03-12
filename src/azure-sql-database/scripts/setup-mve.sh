#!/bin/bash
set -e

# Install mise
(curl https://mise.run | sh)
export PATH="$HOME/.local/bin:$PATH"

# Run mise tasks
mise install -y
uv sync
