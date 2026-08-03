#!/bin/bash
set -e

export PATH="$HOME/.local/bin:$PATH"

mise exec -- firebase emulators:exec ".venv/bin/python main.py"
