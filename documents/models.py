from django.conf import settings
from django.db import models
from parties.models import Party


class Invoice(models.Model):
    number = models.CharField('Hisob-faktura raqami', max_length=64, unique=True)
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name='invoices', verbose_name='Kontragent')
    date = models.DateField('Sana')
    amount = models.DecimalField('Summa', max_digits=16, decimal_places=2)
    currency = models.CharField('Valyuta', max_length=3, choices=settings.CURRENCY_CHOICES, default='UZS')
    description = models.TextField('Tavsif', blank=True)
    file = models.FileField('Fayl (PDF)', upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Hisob-faktura'
        verbose_name_plural = 'Hisob-fakturalar'
        ordering = ['-date']

    def __str__(self):
        return f'{self.number} - {self.party.name}'


class Contract(models.Model):
    number = models.CharField('Shartnoma raqami', max_length=64, unique=True)
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name='contracts', verbose_name='Kontragent')
    start_date = models.DateField('Boshlanish sanasi')
    end_date = models.DateField('Tugash sanasi', null=True, blank=True)
    amount = models.DecimalField('Summa', max_digits=16, decimal_places=2, null=True, blank=True)
    currency = models.CharField('Valyuta', max_length=3, choices=settings.CURRENCY_CHOICES, default='UZS')
    file = models.FileField('Fayl', upload_to='contracts/', blank=True, null=True)
    note = models.TextField('Izoh', blank=True)

    class Meta:
        verbose_name = 'Shartnoma'
        verbose_name_plural = 'Shartnomalar'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.number} - {self.party.name}'
