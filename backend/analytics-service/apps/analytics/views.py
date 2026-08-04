from rest_framework import viewsets, permissions

from .models import AnalyticsItem
from .serializers import AnalyticsItemSerializer


class AnalyticsItemViewSet(viewsets.ModelViewSet):
    """CRUD API for analytics. Replace with real business logic."""

    queryset = AnalyticsItem.objects.all()
    serializer_class = AnalyticsItemSerializer
    permission_classes = [permissions.IsAuthenticated]
