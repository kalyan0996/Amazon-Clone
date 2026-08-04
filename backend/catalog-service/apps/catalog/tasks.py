from celery import shared_task


@shared_task
def example_catalog_task(payload: dict) -> dict:
    """Placeholder async task for the catalog-service."""
    return {"status": "processed", "payload": payload}
