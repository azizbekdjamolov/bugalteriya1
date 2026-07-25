from datetime import date
from decimal import Decimal

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class Party(models.Model):
    class Type(models.TextChoices):
        CUSTOMER = 'customer', 'Mijoz'
        SUPPLIER = 'supplier', "Yetkazib beruvchi"

    type = models.CharField('Turi', max_length=10, choices=Type.choices)
    name = models.CharField('Nomi', max_length=255)
    phone = models.CharField('Telefon', max_length=32, blank=True)
    address = models.CharField('Manzil', max_length=255, blank=True)
    default_currency = models.CharField('Asosiy valyuta', max_length=3, choices=settings.CURRENCY_CHOICES, default='UZS')
    notes = models.TextField('Izoh', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kontragent'
        verbose_name_plural = 'Mijoz / Yetkazib beruvchilar'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'


class Debt(models.Model):
    class Direction(models.TextChoices):
        DEBITOR = 'debitor', 'Debitor (bizga qarzdor)'
        KREDITOR = 'kreditor', 'Kreditor (biz qarzdormiz)'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Faol'
        DUE_SOON = 'due_soon', 'Muddati yaqin'
        OVERDUE = 'overdue', "Muddati o'tgan"
        CLOSED = 'closed', "To'liq yopilgan"

    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name='debts', verbose_name='Kontragent')
    direction = models.CharField('Yo\'nalishi', max_length=10, choices=Direction.choices)
    amount = models.DecimalField('Summa', max_digits=16, decimal_places=2)
    currency = models.CharField('Valyuta', max_length=3, choices=settings.CURRENCY_CHOICES, default='UZS')
    paid_amount = models.DecimalField("To'langan summa", max_digits=16, decimal_places=2, default=0)
    due_date = models.DateField("To'lov muddati")
    description = models.CharField('Izoh', max_length=500, blank=True)
    status = models.CharField('Holati', max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='debts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Qarzdorlik'
        verbose_name_plural = 'Debitor / Kreditor qarzdorlik'
        ordering = ['due_date']

    def __str__(self):
        return f'{self.party.name} - {self.amount} {self.currency} ({self.get_direction_display()})'

    @property
    def remaining_amount(self) -> Decimal:
        return self.amount - self.paid_amount

    @property
    def days_left(self) -> int:
        return (self.due_date - date.today()).days

    def refresh_status(self, save=True):
        """Qolgan summa va muddatga qarab holatni avtomatik yangilaydi."""
        if self.remaining_amount <= 0:
            self.status = self.Status.CLOSED
        else:
            days = self.days_left
            if days < 0:
                self.status = self.Status.OVERDUE
            elif days <= 7:
                self.status = self.Status.DUE_SOON
            else:
                self.status = self.Status.ACTIVE
        if save:
            super(Debt, self).save(update_fields=['status'])

    def save(self, *args, **kwargs):
        if self.remaining_amount <= 0:
            self.status = self.Status.CLOSED
        else:
            days = self.days_left
            if days < 0:
                self.status = self.Status.OVERDUE
            elif days <= 7:
                self.status = self.Status.DUE_SOON
            else:
                self.status = self.Status.ACTIVE
        super().save(*args, **kwargs)
