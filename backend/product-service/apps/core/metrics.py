from django.http import HttpResponse

try:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
except ImportError:  # pragma: no cover
    generate_latest = None
    CONTENT_TYPE_LATEST = "text/plain"


def metrics_view(request):
    if generate_latest is None:
        return HttpResponse("# prometheus_client not installed\n", content_type="text/plain")
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
