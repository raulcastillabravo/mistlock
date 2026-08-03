#!/bin/bash
set -e

mise exec -- firebase emulators:exec ".venv/bin/python main.py"
