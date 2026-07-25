from django.contrib import admin
from .models import Invoice, Contract


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'party', 'date', 'amount', 'currency')
    search_fields = ('number', 'party__name')
    autocomplete_fields = ('party',)
    date_hierarchy = 'date'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'party', 'start_date', 'end_date', 'amount', 'currency')
    search_fields = ('number', 'party__name')
    autocomplete_fields = ('party',)
