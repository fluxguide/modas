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

## STEP - navigate to the docker/ directory (so all relative paths work)
cd "$(dirname "$0")" || exit

## STEP - derive DOMAIN and COMPOSE_PROJECT_NAME from the parent folder name
PARENT_FOLDERNAME=$(basename "$(dirname "$(dirname "$(realpath $0)")")")
DOMAIN="$PARENT_FOLDERNAME"
COMPOSE_PROJECT_NAME="${DOMAIN//./-}"

## STEP - replace all placeholder variables in template files
echo "COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME" > ./.env
set -a
source "$(realpath ./.env)"
set +a

sed "s/{{COMPOSE_PROJECT_NAME}}/$COMPOSE_PROJECT_NAME/g" nginx/nginx.conf > nginx/nginx.conf--generated
sed "s/{{COMPOSE_PROJECT_NAME}}/$COMPOSE_PROJECT_NAME/g" nginx/entrypoint.sh > nginx/entrypoint.sh--generated
sed -e "s/{{COMPOSE_PROJECT_NAME}}/$COMPOSE_PROJECT_NAME/g" \
    -e "s/{{DOMAIN}}/$DOMAIN/g" $COMPOSE_FILE > $COMPOSE_FILE--generated

## STEP - (re-)start docker
docker network ls | grep -w web || docker network create web

if [ -f "$COMPOSE_FILE--previous--generated" ]; then
    docker compose -f $COMPOSE_FILE--previous--generated down
fi

docker compose -f $COMPOSE_FILE--generated up --build --detach

cp $COMPOSE_FILE--generated $COMPOSE_FILE--previous--generated

if [[ "$ENVIRONMENT" == "local" ]]; then
    echo -e "\n\033[1;32m------\n✓ SUCCESS!! Docker containers are up and running.\n✓ http://localhost:8080 \n------\033[0m\n"
else
    echo -e "\n\033[1;32m------\n✓ SUCCESS!! Docker containers are up and running.\n✓ https://$DOMAIN \n------\033[0m\n"
fi
