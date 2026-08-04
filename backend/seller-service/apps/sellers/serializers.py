from rest_framework import serializers

from .models import SellersItem


class SellersItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellersItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
