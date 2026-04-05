#!/bin/bash
set -e

# 1. Install pyenv (via automatic installer)
curl https://pyenv.run | bash

# Configure environment variables for pyenv in the current session
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv init --path)"

# 2. Install Python 3.12 (required by Firebase Emulator)
pyenv install 3.12

# 3. Configure it as global
pyenv global 3.12

# 4. Configure pyenv in .bashrc
CONFIG_LINES='
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
'

echo "$CONFIG_LINES" >> "$HOME/.bashrc"

# Install Firebase tools globally
npm install -g firebase-tools

# Install uv for Python dependency management
pip install uv
uv sync

