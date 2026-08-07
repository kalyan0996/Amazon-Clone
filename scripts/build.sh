#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$HOME/Amazon-Clone"

cd "$ROOT_DIR"

echo "Building backend services..."

for svc_dir in "$ROOT_DIR"/backend/*/; do
    svc=$(basename "$svc_dir")

    if [ -f "$svc_dir/Dockerfile" ]; then
        echo "Building image amazon-clone/$svc:latest"
        docker build -t "amazon-clone/$svc:latest" "$svc_dir"
    else
        echo "Skipping $svc (Dockerfile not found)"
    fi
done

echo "Building frontend..."

docker build \
    -t "amazon-clone/frontend:latest" \
    "$ROOT_DIR/frontend"

echo "====================================="
echo "All Docker images built successfully!"
echo "====================================="
