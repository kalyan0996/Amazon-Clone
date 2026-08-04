#!/usr/bin/env bash
set -euo pipefail
for svc_dir in backend/*/; do
  svc=$(basename "$svc_dir")
  echo "Building image amazon-clone/$svc..."
  docker build -t "amazon-clone/$svc:latest" "$svc_dir"
done
docker build -t amazon-clone/frontend:latest frontend/
