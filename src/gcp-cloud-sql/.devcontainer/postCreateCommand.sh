#!/bin/bash
set -e

# Install uv for Python dependency management
pip3 install uv

# Install Firebase Tools (requires Node.js which is usually in the bookworm image or needs manual install)
# If node is missing, we might need a feature, but usually, we can install via npm.
if ! command -v npm &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

sudo npm install -g firebase-tools

# Sync project dependencies
uv sync

# Setup functions venv
cd functions
uv venv venv
source venv/bin/bin/activate || source venv/bin/activate
uv pip install -r requirements.txt
cd ..

echo "Setup complete!"
