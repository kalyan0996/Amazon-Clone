from rest_framework import viewsets, permissions

from .models import ReviewsItem
from .serializers import ReviewsItemSerializer


class ReviewsItemViewSet(viewsets.ModelViewSet):
    """CRUD API for reviews. Replace with real business logic."""

    queryset = ReviewsItem.objects.all()
    serializer_class = ReviewsItemSerializer
    permission_classes = [permissions.IsAuthenticated]
