from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError


def liveness(request):
    return JsonResponse({"status": "alive", "service": "recommendation-service"})


def readiness(request):
    try:
        conn = connections["default"]
        conn.cursor()
    except OperationalError:
        return JsonResponse({"status": "not_ready", "service": "recommendation-service"}, status=503)
    return JsonResponse({"status": "ready", "service": "recommendation-service"})
