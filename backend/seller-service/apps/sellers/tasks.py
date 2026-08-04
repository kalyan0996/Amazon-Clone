from celery import shared_task


@shared_task
def example_sellers_task(payload: dict) -> dict:
    """Placeholder async task for the seller-service."""
    return {"status": "processed", "payload": payload}
