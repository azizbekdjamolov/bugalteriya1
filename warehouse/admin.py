from django.contrib import admin
from django.utils.html import format_html
from .models import Product, StockMovement


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'quantity', 'min_quantity', 'price', 'stock_badge')
    search_fields = ('name',)

    def stock_badge(self, obj):
        if obj.is_low_stock:
            return format_html('<span style="color:white;background:#dc3545;padding:2px 8px;border-radius:8px;">Kam qoldiq!</span>')
        return format_html('<span style="color:white;background:#28a745;padding:2px 8px;border-radius:8px;">Yetarli</span>')
    stock_badge.short_description = 'Holat'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'type', 'quantity', 'date', 'note')
    list_filter = ('type', 'date')
    autocomplete_fields = ('product',)
