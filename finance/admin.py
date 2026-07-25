from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(SimpleHistoryAdmin):
    list_display = ('date', 'type', 'category', 'amount', 'currency', 'description', 'created_by')
    list_filter = ('type', 'category', 'currency', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'
    autocomplete_fields = ('category',)

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
