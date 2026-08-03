#!/bin/bash
set -e

mise exec -- firebase emulators:exec ".venv/bin/pytest tests/"
