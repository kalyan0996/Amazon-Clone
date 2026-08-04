from rest_framework import serializers

from .models import PricingItem


class PricingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
