from django.contrib import admin
from .models import Employee, SalaryRecord


class SalaryRecordInline(admin.TabularInline):
    model = SalaryRecord
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'phone', 'base_salary', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('full_name',)
    inlines = [SalaryRecordInline]


@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'type', 'amount', 'date', 'note')
    list_filter = ('type', 'date')
    autocomplete_fields = ('employee',)
