from celery import shared_task


@shared_task
def example_payments_task(payload: dict) -> dict:
    """Placeholder async task for the payment-service."""
    return {"status": "processed", "payload": payload}
