from django.db import models


class Employee(models.Model):
    full_name = models.CharField('F.I.Sh.', max_length=255)
    position = models.CharField('Lavozim', max_length=150)
    phone = models.CharField('Telefon', max_length=32, blank=True)
    base_salary = models.DecimalField('Oylik maosh', max_digits=14, decimal_places=2, default=0)
    hired_date = models.DateField('Ishga qabul sanasi', null=True, blank=True)
    is_active = models.BooleanField('Faol', default=True)

    class Meta:
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} - {self.position}'


class SalaryRecord(models.Model):
    class Type(models.TextChoices):
        SALARY = 'salary', 'Oylik'
        BONUS = 'bonus', 'Bonus'
        PENALTY = 'penalty', 'Jarima'
        ADVANCE = 'advance', 'Avans'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_records', verbose_name='Xodim')
    type = models.CharField('Turi', max_length=10, choices=Type.choices)
    amount = models.DecimalField('Summa', max_digits=14, decimal_places=2)
    date = models.DateField('Sana')
    note = models.CharField('Izoh', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Maosh yozuvi'
        verbose_name_plural = 'Maosh tarixi'
        ordering = ['-date']

    def __str__(self):
        return f'{self.employee.full_name} - {self.get_type_display()} - {self.amount}'
