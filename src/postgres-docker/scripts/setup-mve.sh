#!/bin/bash
set -e

# Install mise if not present
(curl https://mise.run | sh)
export PATH="$HOME/.local/bin:$PATH"

# Environment setup
mise install -y
mise run setup

echo "✓ Setup completed successfully!"
