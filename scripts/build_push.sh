#!/usr/bin/env bash
set -euo pipefail

ACR_NAME="perigusacr"
IMAGE_NAME="finance-backend"
IMAGE_TAG="${1:-v0.1.0}"  # allow overriding tag: ./scripts/build_push.sh v0.1.1

ACR_LOGIN_SERVER="${ACR_NAME}.azurecr.io"
FULL_TAG="${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}"

# echo "Tag: ${FULL_TAG}"
# az acr login -n "$ACR_NAME"
# docker build -t "$FULL_TAG" .
# docker push "$FULL_TAG"

az acr build \
  --registry $ACR_NAME \
  --image $IMAGE_NAME:$IMAGE_TAG \
  --platform linux/amd64 \
  --file Dockerfile \
  .