#!/bin/bash
set -e

firebase emulators:exec ".venv/bin/python main.py"
