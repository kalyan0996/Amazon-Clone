from celery import shared_task


@shared_task
def example_search_task(payload: dict) -> dict:
    """Placeholder async task for the search-service."""
    return {"status": "processed", "payload": payload}
