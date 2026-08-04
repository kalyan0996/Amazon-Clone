from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError


def liveness(request):
    return JsonResponse({"status": "alive", "service": "product-service"})


def readiness(request):
    try:
        conn = connections["default"]
        conn.cursor()
    except OperationalError:
        return JsonResponse({"status": "not_ready", "service": "product-service"}, status=503)
    return JsonResponse({"status": "ready", "service": "product-service"})
