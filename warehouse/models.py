from django.db import models


class Product(models.Model):
    name = models.CharField('Nomi', max_length=255)
    unit = models.CharField("O'lchov birligi", max_length=32, default='dona')
    quantity = models.DecimalField('Qoldiq', max_digits=14, decimal_places=2, default=0)
    min_quantity = models.DecimalField('Minimal qoldiq', max_digits=14, decimal_places=2, default=0)
    price = models.DecimalField('Narxi', max_digits=16, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_quantity


class StockMovement(models.Model):
    class Type(models.TextChoices):
        IN = 'in', 'Kirim'
        OUT = 'out', 'Chiqim'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name='Mahsulot')
    type = models.CharField('Turi', max_length=5, choices=Type.choices)
    quantity = models.DecimalField('Miqdori', max_digits=14, decimal_places=2)
    date = models.DateField('Sana')
    note = models.CharField('Izoh', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Ombor harakati'
        verbose_name_plural = 'Kirim / Chiqim'
        ordering = ['-date', '-id']

    def __str__(self):
        return f'{self.product.name} - {self.get_type_display()} - {self.quantity}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            delta = self.quantity if self.type == self.Type.IN else -self.quantity
            Product.objects.filter(pk=self.product_id).update(quantity=models.F('quantity') + delta)
