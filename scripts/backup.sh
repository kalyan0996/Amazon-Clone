#!/usr/bin/env bash
set -euo pipefail
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p backups
for svc_dir in backend/*/; do
  svc=$(basename "$svc_dir")
  echo "Backing up database for $svc..."
  pg_dump "${svc}_db" > "backups/${svc}-${TIMESTAMP}.sql" || true
done
