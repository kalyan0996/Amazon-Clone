#!/usr/bin/env bash
set -euo pipefail
echo "Cleaning up local containers, images and volumes..."
docker compose -f docker-compose.dev.yml down -v --remove-orphans
docker image prune -f
