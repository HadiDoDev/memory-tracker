#!/bin/bash

# Accessing the SERVICES variable and splitting it into an array
#SERVICES="fastapi nginx"
CI_CONTAINER_REGISTRY="$1"
CI_PROJECT_ROOT="$2"
CI_PROJECT_NAME="$3"
CI_STACK_NAME="$4"
CI_SERVICES="$5"

IFS=, read -ra SERVICE_ARRAY <<<"${CI_SERVICES}"

for SERVICE_NAME in "${SERVICE_ARRAY[@]}"; do
  echo "Pull ${SERVICE_NAME} image from repository."
  docker pull "${CI_CONTAINER_REGISTRY}/${SERVICE_NAME}:latest"
done

for SERVICE_NAME in "${SERVICE_ARRAY[@]}"; do
  echo "Update ${SERVICE_NAME} service in ${STACK_NAME} stack."
  docker service update --force "${CI_STACK_NAME}"_"${CI_PROJECT_NAME}"-"${SERVICE_NAME}"
done

docker stack deploy --prune --with-registry-auth -c docker/docker-compose-deploy.yml "${CI_STACK_NAME}"
