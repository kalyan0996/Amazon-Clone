#!/usr/bin/env bash
set -euo pipefail
echo "Bootstrapping full local stack (kind + argocd + services)..."
./infrastructure/kind/create-cluster.sh
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f infrastructure/argocd/app-project.yaml
kubectl apply -f infrastructure/argocd/app-of-apps.yaml
echo "Bootstrap complete."
