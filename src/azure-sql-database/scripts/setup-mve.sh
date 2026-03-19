#!/bin/bash
set -e

(curl https://mise.run | sh)
export PATH="$HOME/.local/bin:$PATH"

mise install -y
mise run install-obdc
mise run setup
mise run init-sql