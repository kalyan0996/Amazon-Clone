from rest_framework import serializers

from .models import ReviewsItem


class ReviewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
