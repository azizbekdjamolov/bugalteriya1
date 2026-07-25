from django.contrib import admin
from .models import CompanySettings


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_currency', 'vat_rate', 'profit_tax_rate')

    def has_add_permission(self, request):
        return not CompanySettings.objects.exists()
