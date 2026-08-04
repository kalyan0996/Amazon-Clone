from rest_framework import serializers

from .models import AuthItem


class AuthItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
