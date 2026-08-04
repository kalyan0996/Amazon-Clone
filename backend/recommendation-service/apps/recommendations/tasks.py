from celery import shared_task


@shared_task
def example_recommendations_task(payload: dict) -> dict:
    """Placeholder async task for the recommendation-service."""
    return {"status": "processed", "payload": payload}
