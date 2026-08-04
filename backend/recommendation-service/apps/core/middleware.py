import logging
import time
import uuid

logger = logging.getLogger("recommendation-service")


class RequestLoggingMiddleware:
    """Attaches a request id and logs basic timing/metadata."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000
        response["X-Request-Id"] = request.id
        logger.info(
            "%s %s -> %s (%.2fms) [%s]",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
            request.id,
        )
        return response
