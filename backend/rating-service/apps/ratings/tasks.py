from celery import shared_task


@shared_task
def example_ratings_task(payload: dict) -> dict:
    """Placeholder async task for the rating-service."""
    return {"status": "processed", "payload": payload}
