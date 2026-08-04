import uuid
from django.db import models


class CartBase(models.Model):
    """Base model for the cart-service domain. Replace with real domain models."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CartItem(CartBase):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cart_item"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
