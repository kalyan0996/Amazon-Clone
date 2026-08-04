from rest_framework import viewsets, permissions

from .models import PaymentsItem
from .serializers import PaymentsItemSerializer


class PaymentsItemViewSet(viewsets.ModelViewSet):
    """CRUD API for payments. Replace with real business logic."""

    queryset = PaymentsItem.objects.all()
    serializer_class = PaymentsItemSerializer
    permission_classes = [permissions.IsAuthenticated]
