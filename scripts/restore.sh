#!/usr/bin/env bash
set -euo pipefail
BACKUP_FILE="${1:?Usage: restore.sh <backup-file>}"
SERVICE="${2:?Usage: restore.sh <backup-file> <service-name>}"
echo "Restoring $SERVICE from $BACKUP_FILE..."
psql "${SERVICE}_db" < "$BACKUP_FILE"
