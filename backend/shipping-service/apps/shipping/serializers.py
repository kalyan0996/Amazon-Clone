from rest_framework import serializers

from .models import ShippingItem


class ShippingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
