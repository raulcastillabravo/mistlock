#!/bin/sh
# Runs AWS Emulator as the owner of the mounted .aws/emulator folder, so it
# can write its credentials and certificate there and the host user (and the
# dev container, which takes the host uid) can read them. Works for any host
# uid (1000 locally, 1001 on GitHub runners) without extra configuration.
set -e

DIR="$HOME/.aws/emulator"
OWNER_UID=$(stat -c %u "$DIR")
OWNER_GID=$(stat -c %g "$DIR")

# Never run the emulator as root
if [ "$OWNER_UID" = "0" ]; then
  OWNER_UID=1000
  OWNER_GID=1000
fi

exec setpriv --reuid "$OWNER_UID" --regid "$OWNER_GID" --clear-groups \
  aws-emulator -b 0.0.0.0 "$@"
