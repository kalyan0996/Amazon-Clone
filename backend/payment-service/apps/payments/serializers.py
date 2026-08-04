from rest_framework import serializers

from .models import PaymentsItem


class PaymentsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentsItem
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
