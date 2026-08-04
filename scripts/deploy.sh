#!/usr/bin/env bash
set -euo pipefail
ENVIRONMENT="${1:-dev}"
echo "Deploying amazon-clone to $ENVIRONMENT..."
kubectl apply -f infrastructure/kubernetes/base/
for svc_dir in backend/*/; do
  kubectl apply -f "${svc_dir}k8s/"
done
