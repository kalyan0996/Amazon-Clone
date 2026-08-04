from celery import shared_task


@shared_task
def example_inventory_task(payload: dict) -> dict:
    """Placeholder async task for the inventory-service."""
    return {"status": "processed", "payload": payload}
