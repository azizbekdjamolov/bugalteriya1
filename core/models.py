from django.db import models


class CompanySettings(models.Model):
    """Sozlamalar bo'limi: kompaniya ma'lumotlari, logo, valyuta, soliq stavkalari."""
    name = models.CharField('Kompaniya nomi', max_length=255, default='Mening kompaniyam')
    logo = models.ImageField('Logo', upload_to='company/', blank=True, null=True)
    base_currency = models.CharField('Asosiy valyuta', max_length=3, default='UZS')
    inn = models.CharField('STIR', max_length=32, blank=True)
    address = models.CharField('Manzil', max_length=255, blank=True)
    phone = models.CharField('Telefon', max_length=32, blank=True)
    vat_rate = models.DecimalField('QQS stavkasi (%)', max_digits=5, decimal_places=2, default=12)
    profit_tax_rate = models.DecimalField('Foyda solig\'i stavkasi (%)', max_digits=5, decimal_places=2, default=15)
    notify_browser_push = models.BooleanField('Brauzer bildirishnomalari yoqilgan', default=True)

    class Meta:
        verbose_name = 'Kompaniya sozlamalari'
        verbose_name_plural = 'Kompaniya sozlamalari'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1  # bitta yagona sozlamalar yozuvi
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
