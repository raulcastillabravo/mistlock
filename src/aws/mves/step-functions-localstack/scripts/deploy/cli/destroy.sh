#!/bin/bash
set -e

export PATH="$HOME/.local/share/mise/shims:$PATH"

set -a
source .env
set +a

deploy/cli/destroy.sh
