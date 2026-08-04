from rest_framework import serializers

from .models import AnalyticsItem


class AnalyticsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
