# Review Service

Django microservice responsible for the **reviews** domain in the amazon-clone platform.

## Run locally

```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8010
```

## Endpoints

- `GET /healthz/` — liveness probe
- `GET /readyz/` — readiness probe
- `GET /metrics/` — Prometheus metrics
- `/api/v1/reviews/items/` — CRUD API (placeholder resource, replace with real domain logic)

## Tests

```bash
python manage.py test
```
