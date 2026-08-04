from django.contrib import admin

from .models import ReviewsItem


@admin.register(ReviewsItem)
class ReviewsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
