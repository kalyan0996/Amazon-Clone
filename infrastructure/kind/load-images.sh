#!/usr/bin/env bash
set -euo pipefail
SERVICES=$(ls ../../backend)
for svc in $SERVICES; do
  echo "Loading amazon-clone/$svc:latest into kind..."
  kind load docker-image "amazon-clone/$svc:latest" --name amazon-clone
done
