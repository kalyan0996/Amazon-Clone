from rest_framework import serializers

from .models import ProductsItem


class ProductsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
