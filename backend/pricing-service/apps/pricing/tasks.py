from celery import shared_task


@shared_task
def example_pricing_task(payload: dict) -> dict:
    """Placeholder async task for the pricing-service."""
    return {"status": "processed", "payload": payload}
