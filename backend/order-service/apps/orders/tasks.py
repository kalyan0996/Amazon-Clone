from celery import shared_task


@shared_task
def example_orders_task(payload: dict) -> dict:
    """Placeholder async task for the order-service."""
    return {"status": "processed", "payload": payload}
