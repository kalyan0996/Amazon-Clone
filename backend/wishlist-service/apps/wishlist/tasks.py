from celery import shared_task


@shared_task
def example_wishlist_task(payload: dict) -> dict:
    """Placeholder async task for the wishlist-service."""
    return {"status": "processed", "payload": payload}
