#!/bin/bash
set -e

firebase emulators:exec ".venv/bin/pytest tests/"
