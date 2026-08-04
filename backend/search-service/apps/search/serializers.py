from rest_framework import serializers

from .models import SearchItem


class SearchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
