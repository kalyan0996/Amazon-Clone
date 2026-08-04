#!/usr/bin/env bash
set -euo pipefail
kind create cluster --config "$(dirname "$0")/kind-config.yaml"
