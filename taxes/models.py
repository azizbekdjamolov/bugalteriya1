from django.db import models


class TaxRecord(models.Model):
    class TaxType(models.TextChoices):
        VAT = 'vat', 'QQS'
        PROFIT = 'profit', 'Foyda solig\'i'
        OTHER = 'other', 'Boshqa'

    tax_type = models.CharField('Soliq turi', max_length=10, choices=TaxType.choices)
    period = models.CharField('Davr (masalan: 2026-Iyul)', max_length=32)
    amount = models.DecimalField('Summa', max_digits=16, decimal_places=2)
    due_date = models.DateField('Topshirish/to\'lov muddati')
    is_paid = models.BooleanField('To\'langan', default=False)
    note = models.CharField('Izoh', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Soliq yozuvi'
        verbose_name_plural = 'Soliqlar'
        ordering = ['due_date']

    def __str__(self):
        return f'{self.get_tax_type_display()} - {self.period} - {self.amount}'


class TaxCalendarEntry(models.Model):
    title = models.CharField('Nomi', max_length=255)
    date = models.DateField('Sana')
    description = models.TextField('Tavsif', blank=True)

    class Meta:
        verbose_name = 'Soliq kalendari yozuvi'
        verbose_name_plural = 'Soliq kalendari'
        ordering = ['date']

    def __str__(self):
        return f'{self.title} ({self.date})'
