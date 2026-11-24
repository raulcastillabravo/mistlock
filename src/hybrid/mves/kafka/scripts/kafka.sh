#!/bin/bash
# Runs any Kafka CLI tool inside a node of the cluster, adding the bootstrap
# servers when the tool needs them.
# Example: scripts/kafka.sh kafka-topics.sh --list
# Use another node while kafka-1 is stopped: KAFKA_NODE=kafka-2 scripts/kafka.sh ...
set -e

NODE="${KAFKA_NODE:-kafka-1}"

BOOTSTRAP=()
[[ "$*" == *"--bootstrap-"* ]] ||
  BOOTSTRAP=(--bootstrap-server kafka-1:9093,kafka-2:9093,kafka-3:9093)

TTY=()
[ -t 0 ] || TTY=(-T)

# The bootstrap goes right after the tool: kafka-metadata-quorum.sh needs it
# before its subcommand
docker compose exec "${TTY[@]}" "$NODE" "/opt/kafka/bin/$1" "${BOOTSTRAP[@]}" "${@:2}"
