from celery import shared_task


@shared_task
def example_cart_task(payload: dict) -> dict:
    """Placeholder async task for the cart-service."""
    return {"status": "processed", "payload": payload}
