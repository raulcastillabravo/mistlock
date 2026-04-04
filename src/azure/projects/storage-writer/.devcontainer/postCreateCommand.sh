#!/bin/bash
set -e

# 1. Install Azure Functions Core Tools via npm
echo "Installing Azure Functions Core Tools..."
npm install -g azure-functions-core-tools@4

# 2. Install Python dependencies with uv
echo "Installing Python dependencies..."
pip3 install uv
uv sync