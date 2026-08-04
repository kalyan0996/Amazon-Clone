from celery import shared_task


@shared_task
def example_shipping_task(payload: dict) -> dict:
    """Placeholder async task for the shipping-service."""
    return {"status": "processed", "payload": payload}
