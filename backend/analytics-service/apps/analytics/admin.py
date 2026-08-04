from django.contrib import admin

from .models import AnalyticsItem


@admin.register(AnalyticsItem)
class AnalyticsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
