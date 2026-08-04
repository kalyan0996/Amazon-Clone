from django.contrib import admin

from .models import RatingsItem


@admin.register(RatingsItem)
class RatingsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
