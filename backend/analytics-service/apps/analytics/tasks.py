from celery import shared_task


@shared_task
def example_analytics_task(payload: dict) -> dict:
    """Placeholder async task for the analytics-service."""
    return {"status": "processed", "payload": payload}
