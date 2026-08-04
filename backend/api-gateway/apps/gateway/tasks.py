from celery import shared_task


@shared_task
def example_gateway_task(payload: dict) -> dict:
    """Placeholder async task for the api-gateway."""
    return {"status": "processed", "payload": payload}
