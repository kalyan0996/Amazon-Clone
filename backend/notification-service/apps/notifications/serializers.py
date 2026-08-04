from rest_framework import serializers

from .models import NotificationsItem


class NotificationsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
