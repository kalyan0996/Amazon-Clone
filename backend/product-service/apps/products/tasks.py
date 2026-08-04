from celery import shared_task


@shared_task
def example_products_task(payload: dict) -> dict:
    """Placeholder async task for the product-service."""
    return {"status": "processed", "payload": payload}
