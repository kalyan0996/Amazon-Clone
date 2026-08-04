from django.contrib import admin

from .models import ProductsItem


@admin.register(ProductsItem)
class ProductsItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at")
    search_fields = ("name",)
