from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'get_full_name', 'role', 'phone', 'is_active_employee', 'is_active')
    list_filter = ('role', 'is_active', 'is_active_employee')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumot', {'fields': ('role', 'phone', 'is_active_employee')}),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'object_repr', 'ip_address')
    list_filter = ('action', 'model_name')
    search_fields = ('object_repr', 'user__username')
    readonly_fields = [f.name for f in AuditLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
