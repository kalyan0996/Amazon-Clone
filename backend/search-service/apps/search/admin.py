from django.contrib import admin

from .models import SearchItem


@admin.register(SearchItem)
class SearchItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
