from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class Category(models.Model):
    class Type(models.TextChoices):
        INCOME = 'income', 'Daromad'
        EXPENSE = 'expense', 'Xarajat'

    name = models.CharField('Nomi', max_length=100)
    type = models.CharField('Turi', max_length=10, choices=Type.choices)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        unique_together = ('name', 'type')

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'


class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOME = 'income', 'Daromad'
        EXPENSE = 'expense', 'Xarajat'

    type = models.CharField('Turi', max_length=10, choices=Type.choices)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions', verbose_name='Kategoriya')
    amount = models.DecimalField('Summa', max_digits=16, decimal_places=2)
    currency = models.CharField('Valyuta', max_length=3, choices=settings.CURRENCY_CHOICES, default='UZS')
    date = models.DateField('Sana')
    description = models.CharField('Izoh', max_length=500, blank=True)
    attachment = models.FileField('Chek/fayl', upload_to='transactions/%Y/%m/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Operatsiya'
        verbose_name_plural = 'Daromad va xarajatlar'
        ordering = ['-date', '-id']

    def __str__(self):
        return f'{self.get_type_display()} - {self.amount} {self.currency} ({self.date})'
