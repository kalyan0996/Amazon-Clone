from rest_framework import viewsets, permissions

from .models import RecommendationsItem
from .serializers import RecommendationsItemSerializer


class RecommendationsItemViewSet(viewsets.ModelViewSet):
    """CRUD API for recommendations. Replace with real business logic."""

    queryset = RecommendationsItem.objects.all()
    serializer_class = RecommendationsItemSerializer
    permission_classes = [permissions.IsAuthenticated]
