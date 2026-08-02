# Amazon Clone — Django Microservices Platform

An enterprise-style, FAANG-pattern e-commerce backend built as 20 independent Django
microservices, containerized, orchestrated on Kubernetes (Kind), deployed via
GitLab CI/CD + ArgoCD, and fully observable with Prometheus/Grafana/Loki/Tempo.

> **Honesty note on scope**: `auth-service`, `product-service`, and `api-gateway` are
> fully implemented with real business logic (JWT/RBAC, catalog + transactional outbox,
> reverse-proxy + rate limiting). The remaining 17 services are scaffolded with the
> identical production-grade skeleton (models, DRF viewsets, JWT verification, health/
> readiness/liveness probes, Prometheus metrics, Swagger, structured logging, tests,
> Dockerfile, full K8s manifest set) plus one representative domain app each — ready
> for you to extend with full business logic per bounded context. See
> [Production Checklist](#production-checklist) for what's stubbed vs. hardened.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Microservices](#microservices)
3. [Folder Structure](#folder-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Environment Variables](#environment-variables)
7. [Database / Redis / RabbitMQ Setup](#database--redis--rabbitmq-setup)
8. [Running Locally (Docker Compose)](#running-locally-docker-compose)
9. [Kind Cluster](#kind-cluster)
10. [Kubernetes](#kubernetes)
11. [Helm](#helm)
12. [ArgoCD](#argocd)
13. [GitLab CI/CD](#gitlab-cicd)
14. [Azure VM Deployment](#azure-vm-deployment)
15. [Observability](#observability)
16. [Security](#security)
17. [Rolling / Canary / Blue-Green](#rolling--canary--blue-green-deployments)
18. [Scaling](#scaling)
19. [Backup & Disaster Recovery](#backup--disaster-recovery)
20. [Useful Commands](#useful-commands)
21. [Expected URLs](#expected-urls)
22. [Troubleshooting](#troubleshooting)
23. [Production Checklist](#production-checklist)
24. [Future Improvements](#future-improvements)

---

## Architecture Overview

```
                                   ┌───────────────────┐
                                   │    Next.js Web     │
                                   └─────────┬──────────┘
                                             │ HTTPS
                                   ┌─────────▼──────────┐
                                   │   NGINX Ingress     │
                                   └─────────┬──────────┘
                                   ┌─────────▼──────────┐
                                   │    api-gateway       │  JWT verify, rate limit, routing
                                   └───┬─────────────┬───┘
              ┌────────────────────────┼─────────────┼───────────────────────┐
      ┌───────▼──────┐         ┌───────▼──────┐             ┌──────▼───────┐
      │ auth-service  │         │product-service│  ...16 more │admin-service │
      │ (own Postgres)│         │(own Postgres) │   services  │(own Postgres)│
      └───────┬──────┘         └───────┬──────┘             └──────┬───────┘
              │   RabbitMQ (events, outbox relay, DLQ, Celery tasks)               │
              └────────────────────────┴─────────────────────────────┴────────────┘
                                             │
                          ┌──────────────────┼──────────────────┐
                    ┌─────▼─────┐     ┌──────▼──────┐    ┌──────▼──────┐
                    │ Prometheus │     │ Loki+Promtail│    │ Tempo (OTel) │
                    │  Grafana   │     │   (logs)     │    │  (traces)    │
                    └────────────┘     └──────────────┘    └──────────────┘
```

**Key patterns applied:**
- **Database-per-service** — no shared schema, no cross-service foreign keys; services
  reference each other only by ID and communicate via REST or async events.
- **Stateless JWT verification** — only `auth-service` owns user credentials; every other
  service verifies the JWT signature/claims without a network call or shared DB (see
  `apps/core/authentication.py` in `product-service` for the reference implementation).
- **Transactional Outbox + Saga** — writes that must trigger cross-service side effects
  write an `OutboxEvent` row in the same DB transaction, relayed to RabbitMQ by a Celery
  beat task, with retry + dead-letter-exchange on exhaustion (see `product-service`).
- **12-Factor config** — all services read config from environment variables /
  `.env` files, never hardcoded.

## Microservices

| Service | Port (compose) | Owns DB | Status |
|---|---|---|---|
| api-gateway | 8080 | — | Implemented (reverse proxy, JWT pass-through, rate limiting) |
| auth-service | 8001 | auth_db | Implemented (JWT, RBAC/ABAC, Argon2, brute-force protection) |
| product-service | 8002 | product_db | Implemented (catalog, outbox pattern, Celery relay) |
| user-service | 8003 | user_db | Scaffolded (profile domain app) |
| category-service | 8004 | category_db | Scaffolded |
| inventory-service | 8005 | inventory_db | Scaffolded |
| cart-service | 8006 | cart_db | Scaffolded |
| wishlist-service | 8007 | wishlist_db | Scaffolded |
| order-service | 8008 | order_db | Scaffolded |
| payment-service | 8009 | payment_db | Scaffolded |
| shipping-service | 8010 | shipping_db | Scaffolded |
| notification-service | 8011 | notification_db | Scaffolded |
| review-service | 8012 | review_db | Scaffolded |
| search-service | 8013 | search_db | Scaffolded |
| recommendation-service | 8014 | recommendation_db | Scaffolded |
| coupon-service | 8015 | coupon_db | Scaffolded |
| seller-service | 8016 | seller_db | Scaffolded |
| analytics-service | 8017 | analytics_db | Scaffolded |
| audit-service | 8018 | audit_db | Scaffolded |
| admin-service | 8019 | admin_db | Scaffolded |

"Scaffolded" = real Django project, real DRF app with one domain model + CRUD, JWT auth,
health/metrics/swagger, tests, Dockerfile, full K8s manifests, Helm-ready — not a hollow
stub — but without the complete business logic of a production checkout/payment/etc. flow.

## Folder Structure

```
amazon-clone/
├── backend/
│   ├── api-gateway/ ... admin-service/     # 20 Django microservices
│   │   ├── apps/<domain>/                  # models, serializers, views, urls, tasks, admin
│   │   ├── apps/core/                      # health, metrics, middleware, JWT auth, exceptions
│   │   ├── config/                         # settings, urls, wsgi, asgi, celery
│   │   ├── k8s/                            # deployment, service, configmap, secret, ingress,
│   │   │                                     hpa, networkpolicy, pdb, serviceaccount, role(binding)
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt / pyproject.toml
│   │   ├── .env.example
│   │   └── README.md
│   └── ...
├── frontend/                               # Next.js app (see frontend/README.md)
├── infrastructure/
│   ├── docker/nginx/                       # reverse proxy conf
│   ├── kind/                               # kind-config.yaml, create/delete/load scripts
│   ├── kubernetes/base/                    # namespace, storageclass, PV/PVC, clusterrole(binding)
│   ├── helm/service-chart/                 # parameterized chart template (copy per service)
│   └── argocd/                             # AppProject, app-of-apps, one Application per service
├── monitoring/                             # prometheus.yml, alert.rules.yml, alertmanager.yml, tempo.yml
├── logging/                                # loki-config.yml, promtail-config.yml
├── scripts/                                # setup/build/test/deploy/rollback/backup/restore/cleanup/bootstrap
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── docker-compose.monitoring.yml
├── docker-compose.tools.yml
├── .gitlab-ci.yml
└── README.md                               # this file
```

## Prerequisites

- Docker Engine ≥ 24 & Docker Compose v2
- Python 3.13
- kubectl ≥ 1.29
- Kind ≥ 0.23
- Helm ≥ 3.14
- ArgoCD CLI (optional, for CLI-based sync)
- GitLab Runner (for CI/CD, if self-hosting)
- Node.js ≥ 20 (for the Next.js frontend)

## Installation

### Python Setup (per service, for local non-Docker dev)
```bash
cd backend/auth-service
python3.13 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

### Docker Setup
```bash
docker --version && docker compose version
```

### Docker Compose (full local stack)
```bash
./scripts/setup.sh
# equivalent to:
docker compose -f docker-compose.dev.yml up -d --build
```

## Environment Variables

Every service ships a `.env.example` — copy to `.env` before running. Shared conventions:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` locally, `False` in staging/prod |
| `DB_HOST` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_PORT` | Service's own Postgres |
| `REDIS_URL` | Cache backend (separate DB index per service) |
| `RABBITMQ_URL` / `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` | Async messaging |
| `JWT_SIGNING_KEY` | Must match `auth-service`'s key — HS256 shared secret in this reference implementation (swap to RS256 + JWKS endpoint for production; see Production Checklist) |
| `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` | Frontend origin allowlist |
| `OTEL_EXPORTER_OTLP_ENDPOINT` / `OTEL_SERVICE_NAME` | Tracing export target |
| `SENTRY_DSN` | Optional error tracking |

## Database / Redis / RabbitMQ Setup

`docker-compose.dev.yml` provisions one PostgreSQL container **per service** (true
database-per-service isolation), plus one shared `redis` (namespaced by DB index per
service) and one shared `rabbitmq` (namespaced by exchange/routing key per service).

```bash
# Run migrations for every service after first boot:
for svc in backend/*/; do
  docker compose -f docker-compose.dev.yml exec "$(basename "$svc")" python manage.py migrate
done
```

## Running Locally (Docker Compose)

```bash
docker compose -f docker-compose.dev.yml up -d --build      # app + per-service DBs + redis + rabbitmq
docker compose -f docker-compose.monitoring.yml up -d       # prometheus, grafana, alertmanager, tempo, node-exporter
docker compose -f docker-compose.tools.yml up -d            # pgadmin / other dev tools
docker compose -f docker-compose.dev.yml logs -f auth-service
```

`docker-compose.prod.yml` swaps dev ergonomics for Gunicorn-only, resource limits, and
no bind-mounted source — a reference for a single-VM Compose production deploy (see
Azure VM Deployment); the Kind/K8s path below is the primary production target.

## Kind Cluster

```bash
cd infrastructure/kind
./kind-create.sh          # cluster + nginx ingress + namespaces + storageclass
./kind-load-images.sh     # docker build + kind load for all 20 services
./kind-delete.sh          # teardown
```

## Kubernetes

Each service ships its own manifest set under `backend/<service>/k8s/`:
`deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`, `ingress.yaml`,
`hpa.yaml`, `networkpolicy.yaml`, `pdb.yaml`, `serviceaccount.yaml`, `role.yaml`,
`rolebinding.yaml`. Cluster-scoped resources (`namespace`, `storageclass`,
PV/PVC, `clusterrole`/`clusterrolebinding`) live in `infrastructure/kubernetes/base/`.

```bash
kubectl apply -f infrastructure/kubernetes/base/
kubectl apply -f backend/auth-service/k8s/
kubectl apply -f backend/product-service/k8s/
# ...repeat per service, or use scripts/deploy.sh which loops over all of them
kubectl -n amazon-clone get pods
```

## Helm

A single parameterized chart (`infrastructure/helm/service-chart/`) is used for every
service — copy it per-service or maintain a `values.yaml` per service. See
`infrastructure/helm/service-chart/README.md`.

```bash
helm install auth-service infrastructure/helm/service-chart -n amazon-clone \
  --set serviceName=auth-service --set image.repository=amazon-clone/auth-service
```

## ArgoCD

App-of-Apps pattern: one root `Application` (`infrastructure/argocd/app-of-apps.yaml`)
watches `infrastructure/argocd/apps/`, which contains one child `Application` per
microservice, each with `automated: {prune: true, selfHeal: true}`.

```bash
kubectl apply -f infrastructure/argocd/projects/amazon-clone-project.yaml
kubectl apply -f infrastructure/argocd/app-of-apps.yaml
argocd app list
argocd app sync auth-service
```

## GitLab CI/CD

`.gitlab-ci.yml` stages: `lint → format → test → coverage → security → build → push →
deploy-dev → deploy-staging → deploy-production (manual) → rollback (manual)`.

Security stage runs: Black, isort, Flake8, Ruff, Bandit, Safety, OWASP Dependency-Check,
Semgrep, TruffleHog (secret detection), Trivy (filesystem + image), Grype, Docker Scout,
Syft (SBOM), and a license check. `test` runs as a parallel matrix across all 20 services
against ephemeral Postgres/Redis services.

## Azure VM Deployment

```bash
# --- On a fresh Ubuntu 22.04/24.04 Azure VM ---
sudo apt-get update && sudo apt-get upgrade -y

# Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER && newgrp docker

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# ArgoCD CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd

# GitLab Runner
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt-get install gitlab-runner -y
sudo gitlab-runner register   # paste your project's registration token
```

### Azure NSG Rules (via Azure CLI)
```bash
RG=amazon-clone-rg; NSG=amazon-clone-nsg
for p in 80:HTTP 443:HTTPS 6443:K8sAPI 9090:Prometheus 3000:Grafana 16686:Tempo 5672:RabbitMQ 5432:Postgres 6379:Redis; do
  PORT="${p%%:*}"; NAME="${p##*:}"
  az network nsg rule create -g "$RG" --nsg-name "$NSG" -n "Allow-${NAME}" \
    --priority $((1000 + PORT)) --direction Inbound --access Allow --protocol Tcp \
    --destination-port-ranges "$PORT" --source-address-prefixes Internet
done
az network nsg rule create -g "$RG" --nsg-name "$NSG" -n "Allow-NodePort" \
  --priority 1100 --direction Inbound --access Allow --protocol Tcp \
  --destination-port-ranges 30000-32767 --source-address-prefixes Internet
```

### UFW (host firewall, in addition to NSG)
```bash
sudo ufw allow 80/tcp 443/tcp 6443/tcp 9090/tcp 3000/tcp 16686/tcp 5672/tcp 5432/tcp 6379/tcp
sudo ufw allow 30000:32767/tcp
sudo ufw enable
```

### Port List
| Port | Purpose |
|---|---|
| 80 / 443 | HTTP/HTTPS ingress |
| 6443 | Kubernetes API server |
| 30000-32767 | NodePort range |
| 9090 | Prometheus |
| 3000 | Grafana |
| 16686 | Tempo query UI |
| 5672 (15672 mgmt) | RabbitMQ |
| 5432 | PostgreSQL |
| 6379 | Redis |

## Observability

- **Prometheus** (`monitoring/prometheus/prometheus.yml`) scrapes every service's
  `/metrics` (via `django-prometheus`), Node Exporter, and Kube State Metrics.
- **Alertmanager** (`monitoring/alertmanager/alertmanager.yml`) routes alerts from
  `alert.rules.yml` (error-rate, latency, pod-restart, disk pressure rules).
- **Grafana** — point at the Prometheus + Loki + Tempo datasources; dashboards are
  environment-specific (import via provisioning or the UI).
- **Loki + Promtail** (`logging/`) ship structured JSON logs (with `correlation_id`)
  from every container.
- **Tempo + OpenTelemetry** (`monitoring/tempo/tempo.yml`) collect distributed traces;
  each service is instrumented via `opentelemetry-instrumentation-django`.

## Security

Implemented in the reference services and scaffolded identically across all 20:
OWASP-aligned headers (HSTS, X-Frame-Options, nosniff, referrer policy), CORS/CSRF
allowlists, DRF throttling (rate limiting), JWT short-lived access + rotating refresh
tokens with blacklist-on-logout, RBAC via role claims + ABAC-style condition objects on
`Permission`, Argon2 password hashing + complexity validator, `django-axes` brute-force
lockout, structured audit-friendly logging with correlation IDs, non-root Docker users,
Kubernetes `NetworkPolicy` default-deny-except-declared, `Secret`-based credential
injection (swap for Vault/Sealed-Secrets/Azure Key Vault CSI in production — see
Production Checklist).

## Rolling / Canary / Blue-Green Deployments

- **Rolling** (default): `kubectl set image` / `helm upgrade` — Deployment's default
  `RollingUpdate` strategy, gated by `readinessProbe` + `PodDisruptionBudget`.
- **Canary**: run a second Deployment (`auth-service-canary`) behind the same Service
  selector with a small replica count; shift traffic by adjusting relative replica
  counts, or adopt Argo Rollouts for weighted traffic + automated analysis.
- **Blue-Green**: deploy `auth-service-green` alongside `auth-service-blue`, validate,
  then flip the Service `selector` (or Ingress backend) to the new color.

## Scaling

`hpa.yaml` per service targets 70% CPU / 80% memory, `minReplicas: 2` /
`maxReplicas: 10`. Tune per service based on load-test results; pair with
`PodDisruptionBudget` (`minAvailable: 1`) so scale-down/node-drain never drops to zero.

## Backup & Disaster Recovery

```bash
./scripts/backup.sh                          # pg_dump every service DB -> backups/<timestamp>/*.sql.gz
./scripts/restore.sh backups/<ts>/auth_db.sql.gz auth_db
```
For DR beyond a single VM: enable Postgres WAL archiving / managed Azure Database for
PostgreSQL with point-in-time restore, and replicate RabbitMQ/Redis via managed services
or clustering in production.

## Useful Commands

**kubectl**
```bash
kubectl -n amazon-clone get pods -w
kubectl -n amazon-clone logs -f deploy/auth-service
kubectl -n amazon-clone exec -it deploy/auth-service -- python manage.py shell
kubectl -n amazon-clone rollout restart deploy/auth-service
kubectl -n amazon-clone top pods
```

**Docker / Compose**
```bash
docker compose -f docker-compose.dev.yml ps
docker compose -f docker-compose.dev.yml exec auth-service python manage.py createsuperuser
docker compose -f docker-compose.dev.yml down -v
```

**Kind**
```bash
kind get clusters
kind export kubeconfig --name amazon-clone
```

**Helm**
```bash
helm list -n amazon-clone
helm upgrade auth-service infrastructure/helm/service-chart -n amazon-clone
helm rollback auth-service 1 -n amazon-clone
```

**ArgoCD**
```bash
argocd login <argocd-server>
argocd app sync amazon-clone-root
argocd app history auth-service
```

**GitLab**
```bash
git push origin main            # triggers full pipeline
gitlab-runner verify
```

## Expected URLs

| Service | Local (Compose) | Swagger |
|---|---|---|
| api-gateway | http://localhost:8080 | http://localhost:8080/api/docs/ |
| auth-service | http://localhost:8001 | http://localhost:8001/api/docs/ |
| product-service | http://localhost:8002 | http://localhost:8002/api/docs/ |
| Grafana | http://localhost:3000 | — |
| Prometheus | http://localhost:9090 | — |
| RabbitMQ mgmt | http://localhost:15672 | — |
| Tempo query | http://localhost:16686 | — |

On Kind/K8s, everything is reachable through the ingress host
`api.amazon-clone.local` (add to `/etc/hosts`), path-routed per service
(e.g. `/auth/...`, `/catalog/...`).

## Troubleshooting

**Common Errors**
- `CrashLoopBackOff` on a service → check `kubectl logs`, usually missing migration or
  bad `Secret` value; run `python manage.py migrate` manually via `kubectl exec`.
- `502` at the ingress → target Service has no Ready endpoints; check readiness probe
  path matches `apps/core/urls.py`.
- JWT `401` across services → `JWT_SIGNING_KEY` mismatch between `auth-service` and the
  calling service's `.env`/`Secret`.
- Kind image not found → forgot `kind load docker-image`; run
  `infrastructure/kind/kind-load-images.sh`.

**Performance Tuning**
- Increase Gunicorn `--workers`/`--threads` per service based on CPU request; tune
  `CONN_MAX_AGE` and connection pooling (e.g. PgBouncer) under high DB load; add Redis
  caching for read-heavy endpoints (product listing, category tree); scale Celery
  worker concurrency for outbox relay backlog.

## Production Checklist

- [ ] Swap HS256 shared-secret JWT verification for RS256 + JWKS endpoint on
      `auth-service` so services never hold a shared signing secret.
- [ ] Replace plaintext K8s `Secret`s with Vault / Sealed Secrets / Azure Key Vault CSI.
- [ ] Complete business logic for the 17 scaffolded services (order/payment/shipping
      sagas, coupon rules engine, search indexing, recommendation model, etc).
- [ ] Add per-service Saga orchestration/choreography for the checkout flow (order →
      payment → inventory reservation → shipping) with compensating transactions.
- [ ] Wire SonarQube (referenced in requirements) into `.gitlab-ci.yml` security stage
      once a SonarQube server URL/token is available.
- [ ] Add Terraform for actual Azure infra provisioning (`infrastructure/terraform/` is
      reserved but not populated — this repo assumes a pre-existing Ubuntu VM).
- [ ] Load-test (k6/Locust) to right-size HPA thresholds and resource requests/limits.
- [ ] Enable TLS everywhere (cert-manager + Let's Encrypt or internal CA) — ingress
      manifests are HTTP-only by default here.

## Future Improvements

- Argo Rollouts for native canary/blue-green with automated metric analysis.
- Multi-cluster / multi-region ArgoCD ApplicationSets.
- GraphQL federation layer alongside REST in `api-gateway`.
- Event schema registry (e.g. Avro + Schema Registry) for RabbitMQ payload contracts.
- OpenFeature-based feature flagging per service.
