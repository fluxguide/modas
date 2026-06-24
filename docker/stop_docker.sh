#!/bin/bash

## STEP - validate dependencies of this script
for cmd in docker uname grep sed; do
  command -v "$cmd" >/dev/null && continue
  echo "Ooops! Required command $cmd not found on the system."
  exit 1
done

## STEP - define ENVIRONMENT ("local" or "server")
OS_NAME="$(uname)"
if [ "$OS_NAME" = "Darwin" ]; then
    ENVIRONMENT="local"
else
    ENVIRONMENT="server"
fi

## STEP - Determine the docker-compose.yml file (by environment)
if [[ "$ENVIRONMENT" == "local" || "$ENVIRONMENT" == "server" ]]; then
    COMPOSE_FILE="docker-compose.$ENVIRONMENT.yml"
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        echo "File $COMPOSE_FILE does not exist."
        exit 1
    fi
else
    echo "Unknown environment: $ENVIRONMENT"
    exit 1
fi

cd "$(dirname "$0")" || exit

if [ -f "$COMPOSE_FILE--previous--generated" ]; then
    docker compose -f $COMPOSE_FILE--previous--generated down
fi
