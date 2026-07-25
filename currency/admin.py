from django.contrib import admin
from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency_code', 'rate', 'diff', 'date')
    list_filter = ('currency_code',)
    date_hierarchy = 'date'
