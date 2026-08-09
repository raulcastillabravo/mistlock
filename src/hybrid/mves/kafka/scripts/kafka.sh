#!/bin/bash
# Runs any Kafka CLI tool inside the broker container, adding the bootstrap
# server when the tool needs it.
# Example: scripts/kafka.sh kafka-topics.sh --list
set -e

BOOTSTRAP=()
[[ "$*" == *"--bootstrap-server"* ]] || BOOTSTRAP=(--bootstrap-server 127.0.0.1:9092)

TTY=()
[ -t 0 ] && TTY=(-t)

docker exec -i "${TTY[@]}" kafka "/opt/kafka/bin/$1" "${@:2}" "${BOOTSTRAP[@]}"
