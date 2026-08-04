from celery import shared_task


@shared_task
def example_users_task(payload: dict) -> dict:
    """Placeholder async task for the user-service."""
    return {"status": "processed", "payload": payload}
