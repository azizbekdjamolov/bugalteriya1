from django.contrib import admin
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from .models import Party, Debt

STATUS_COLORS = {
    'active': '#28a745',
    'due_soon': '#ffc107',
    'overdue': '#dc3545',
    'closed': '#6c757d',
}


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'phone', 'default_currency')
    list_filter = ('type', 'default_currency')
    search_fields = ('name', 'phone')


@admin.register(Debt)
class DebtAdmin(SimpleHistoryAdmin):
    list_display = ('party', 'direction', 'amount', 'currency', 'paid_amount', 'remaining_amount_display',
                     'due_date', 'status_badge')
    list_filter = ('direction', 'status', 'currency')
    search_fields = ('party__name', 'description')
    autocomplete_fields = ('party',)
    date_hierarchy = 'due_date'

    def remaining_amount_display(self, obj):
        return f'{obj.remaining_amount:,.2f}'
    remaining_amount_display.short_description = 'Qolgan summa'

    def status_badge(self, obj):
        color = STATUS_COLORS.get(obj.status, '#333')
        return format_html('<span style="color:white;background:{};padding:2px 8px;border-radius:8px;">{}</span>',
                            color, obj.get_status_display())
    status_badge.short_description = 'Holati'

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
