from django.contrib import admin
from django.urls import path, include

from apps.core.health import liveness, readiness
from apps.core.metrics import metrics_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", liveness, name="liveness"),
    path("readyz/", readiness, name="readiness"),
    path("metrics/", metrics_view, name="metrics"),
    path("api/v1/gateway/", include("apps.gateway.urls")),
]
