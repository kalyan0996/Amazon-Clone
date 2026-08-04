from rest_framework import serializers

from .models import UsersItem


class UsersItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
