#!/bin/bash

echo Services: "${CI_SERVICES}"
IFS=, read -ra SERVICE_ARRAY <<<"$CI_SERVICES"

for SERVICE_NAME in "${SERVICE_ARRAY[@]}"; do
  echo "Push ${SERVICE_NAME} image to repository."
  docker push "${CI_CONTAINER_REGISTRY}/${SERVICE_NAME}:latest"
done
