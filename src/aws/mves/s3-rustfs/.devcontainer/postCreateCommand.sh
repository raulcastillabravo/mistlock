#!/bin/bash
set -e

scripts/setup.sh

# Add mise to PATH
MISE_SHIMS="$HOME/.local/share/mise/shims"
EXPORT_LINE="export PATH=\$PATH:$MISE_SHIMS"

for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [ -f "$RC" ] && ! grep -qF "$MISE_SHIMS" "$RC"; then
    echo "$EXPORT_LINE" >> "$RC"
  fi
done
