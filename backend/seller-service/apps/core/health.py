from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError


def liveness(request):
    return JsonResponse({"status": "alive", "service": "seller-service"})


def readiness(request):
    try:
        conn = connections["default"]
        conn.cursor()
    except OperationalError:
        return JsonResponse({"status": "not_ready", "service": "seller-service"}, status=503)
    return JsonResponse({"status": "ready", "service": "seller-service"})
