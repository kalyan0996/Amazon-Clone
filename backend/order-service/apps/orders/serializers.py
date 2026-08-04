from rest_framework import serializers

from .models import OrdersItem


class OrdersItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
