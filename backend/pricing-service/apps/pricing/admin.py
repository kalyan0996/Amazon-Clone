from django.contrib import admin

from .models import PricingItem


@admin.register(PricingItem)
class PricingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
