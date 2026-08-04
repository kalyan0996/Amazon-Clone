# Amazon Clone — Microservices Platform

A scaffolded, Kubernetes-native e-commerce platform: 20 Django microservices behind
an API gateway, a Next.js storefront, and full GitOps/observability tooling.

> **Note:** this is a project **scaffold**. Structure, configuration, health checks,
> Docker/K8s/Helm/ArgoCD manifests, and CI are complete and functional; domain business
> logic inside each service (`apps/<domain>/models.py` etc.) is a placeholder ready to
> be built out.

## Services

- `api-gateway` — gateway domain (port 8000)
- `auth-service` — auth domain (port 8001)
- `user-service` — users domain (port 8002)
- `product-service` — products domain (port 8003)
- `catalog-service` — catalog domain (port 8004)
- `inventory-service` — inventory domain (port 8005)
- `cart-service` — cart domain (port 8006)
- `order-service` — orders domain (port 8007)
- `payment-service` — payments domain (port 8008)
- `shipping-service` — shipping domain (port 8009)
- `review-service` — reviews domain (port 8010)
- `rating-service` — ratings domain (port 8011)
- `recommendation-service` — recommendations domain (port 8012)
- `search-service` — search domain (port 8013)
- `notification-service` — notifications domain (port 8014)
- `wishlist-service` — wishlist domain (port 8015)
- `seller-service` — sellers domain (port 8016)
- `pricing-service` — pricing domain (port 8017)
- `analytics-service` — analytics domain (port 8018)
- `admin-service` — admin_panel domain (port 8019)

## Repository layout

See the top-level directories: `backend/`, `frontend/`, `infrastructure/`, `monitoring/`,
`logging/`, `scripts/`.

## Quickstart (Docker Compose)

```bash
docker compose -f docker-compose.dev.yml up --build
```

Frontend: http://localhost:3000
API gateway: http://localhost:8000

## Quickstart (local Kubernetes via kind)

```bash
./scripts/bootstrap.sh   # creates kind cluster + installs ArgoCD
./scripts/build.sh       # builds all service images
./infrastructure/kind/load-images.sh
./scripts/deploy.sh dev
```

## Observability

```bash
docker compose -f docker-compose.monitoring.yml up -d
```

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001
- Loki/Promtail: log aggregation
- Tempo: distributed tracing

## Dev tools

```bash
docker compose -f docker-compose.tools.yml up -d
```

pgAdmin (5050), Redis Commander (8081), MailHog (8025).

## CI/CD

`.gitlab-ci.yml` runs lint → test → build → deploy across all services and the frontend.
ArgoCD (`infrastructure/argocd/`) syncs each service's `k8s/` manifests as a separate
Application, orchestrated by an app-of-apps.
