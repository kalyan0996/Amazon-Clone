from celery import shared_task


@shared_task
def example_reviews_task(payload: dict) -> dict:
    """Placeholder async task for the review-service."""
    return {"status": "processed", "payload": payload}
