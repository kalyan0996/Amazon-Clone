from rest_framework import viewsets, permissions

from .models import RatingsItem
from .serializers import RatingsItemSerializer


class RatingsItemViewSet(viewsets.ModelViewSet):
    """CRUD API for ratings. Replace with real business logic."""

    queryset = RatingsItem.objects.all()
    serializer_class = RatingsItemSerializer
    permission_classes = [permissions.IsAuthenticated]
