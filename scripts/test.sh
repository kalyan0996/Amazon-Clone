#!/usr/bin/env bash
set -euo pipefail
for svc_dir in backend/*/; do
  svc=$(basename "$svc_dir")
  echo "Testing $svc..."
  (cd "$svc_dir" && .venv/bin/python manage.py test)
done
(cd frontend && npm test)
