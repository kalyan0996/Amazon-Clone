from celery import shared_task


@shared_task
def example_notifications_task(payload: dict) -> dict:
    """Placeholder async task for the notification-service."""
    return {"status": "processed", "payload": payload}
