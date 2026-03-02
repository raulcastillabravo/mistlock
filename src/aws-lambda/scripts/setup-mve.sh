#!/bin/bash
set -e

echo "1. Installing mise and uv..."
(curl https://mise.run | sh) || (winget install jdx.mise) || echo "✓ mise check complete"
(curl -LsSf https://astral.sh/uv/install.sh | sh) || echo "✓ uv check complete"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.local/share/mise/shims:$PATH"

echo "2. Installing tools from mise.toml..."
mise install -y

echo "3. Configuring LocalStack profile for AWS CLI..."
aws configure set aws_access_key_id test --profile localstack
aws configure set aws_secret_access_key test --profile localstack
aws configure set region us-east-1 --profile localstack
aws configure set output json --profile localstack
aws configure set endpoint_url http://localhost:4566 --profile localstack
aws configure set cli_pager "" --profile localstack

echo "4. Setting up Python environment with uv..."
uv sync

echo "✓ Setup completed successfully!"
