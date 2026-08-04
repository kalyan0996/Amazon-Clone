import uuid
from django.db import models


class ReviewsBase(models.Model):
    """Base model for the review-service domain. Replace with real domain models."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ReviewsItem(ReviewsBase):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "reviews_item"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
