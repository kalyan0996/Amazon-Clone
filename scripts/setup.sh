#!/usr/bin/env bash
set -euo pipefail
echo "Setting up amazon-clone dev environment..."
for svc_dir in backend/*/; do
  svc=$(basename "$svc_dir")
  echo "Installing deps for $svc..."
  (cd "$svc_dir" && python -m venv .venv && .venv/bin/pip install -r requirements.txt)
done
(cd frontend && npm install)
echo "Setup complete."
