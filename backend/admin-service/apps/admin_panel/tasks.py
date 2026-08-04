from celery import shared_task


@shared_task
def example_admin_panel_task(payload: dict) -> dict:
    """Placeholder async task for the admin-service."""
    return {"status": "processed", "payload": payload}
