from rest_framework import serializers

from .models import AdminPanelItem


class AdminPanelItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPanelItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
