from rest_framework import serializers

from .models import RatingsItem


class RatingsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingsItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
