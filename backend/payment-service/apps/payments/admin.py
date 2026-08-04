from django.contrib import admin

from .models import PaymentsItem


@admin.register(PaymentsItem)
class PaymentsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
