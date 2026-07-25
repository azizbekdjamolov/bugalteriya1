from django.contrib import admin
from .models import TaxRecord, TaxCalendarEntry


@admin.register(TaxRecord)
class TaxRecordAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'period', 'amount', 'due_date', 'is_paid')
    list_filter = ('tax_type', 'is_paid')
    date_hierarchy = 'due_date'


@admin.register(TaxCalendarEntry)
class TaxCalendarEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    date_hierarchy = 'date'
