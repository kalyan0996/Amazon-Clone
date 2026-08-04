from celery import shared_task


@shared_task
def example_auth_task(payload: dict) -> dict:
    """Placeholder async task for the auth-service."""
    return {"status": "processed", "payload": payload}
