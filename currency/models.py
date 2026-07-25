from django.db import models


class ExchangeRate(models.Model):
    currency_code = models.CharField('Valyuta', max_length=3)
    rate = models.DecimalField("Kursi (UZS)", max_digits=16, decimal_places=4)
    diff = models.DecimalField('Kurs farqi', max_digits=10, decimal_places=4, default=0)
    date = models.DateField('Sana')

    class Meta:
        verbose_name = 'Valyuta kursi'
        verbose_name_plural = "Valyuta kurslari (Markaziy bank)"
        unique_together = ('currency_code', 'date')
        ordering = ['-date', 'currency_code']

    def __str__(self):
        return f'{self.currency_code}: {self.rate} ({self.date})'

    @classmethod
    def latest_date(cls):
        latest = cls.objects.order_by('-date').first()
        return latest.date if latest else None
