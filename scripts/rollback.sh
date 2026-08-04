#!/usr/bin/env bash
set -euo pipefail
SERVICE="${1:?Usage: rollback.sh <service-name>}"
echo "Rolling back $SERVICE..."
kubectl rollout undo "deployment/$SERVICE" -n amazon-clone
