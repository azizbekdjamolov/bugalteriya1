from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        DIRECTOR = 'director', 'Direktor'
        ACCOUNTANT = 'accountant', 'Buxgalter'
        MANAGER = 'manager', 'Menejer'
        AUDITOR = 'auditor', 'Auditor (faqat ko\'rish)'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ACCOUNTANT)
    phone = models.CharField(max_length=32, blank=True)
    is_active_employee = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_readonly(self):
        return self.role == self.Role.AUDITOR

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN or self.is_superuser


class AuditLog(models.Model):
    """Kim, qachon, nimani o'zgartirgani haqida yozuv (xavfsizlik talabi)."""
    class Action(models.TextChoices):
        CREATE = 'create', "Qo'shildi"
        UPDATE = 'update', 'Tahrirlandi'
        DELETE = 'delete', "O'chirildi"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=10, choices=Action.choices)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64, blank=True)
    object_repr = models.CharField(max_length=255, blank=True)
    changes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Audit jurnali'
        verbose_name_plural = 'Audit jurnali'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user} - {self.get_action_display()} - {self.model_name}'
