from django.contrib import admin

from .models import RecommendationsItem


@admin.register(RecommendationsItem)
class RecommendationsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
