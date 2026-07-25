from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Level(models.TextChoices):
        RED = 'red', "Qizil (muddati o'tgan)"
        ORANGE = 'orange', "To'q sariq (1 kun qoldi)"
        YELLOW = 'yellow', 'Sariq (3-7 kun qoldi)'
        GREEN = 'green', 'Yashil (yangi xabar)'

    title = models.CharField('Sarlavha', max_length=255)
    message = models.TextField('Xabar matni')
    level = models.CharField('Darajasi', max_length=10, choices=Level.choices, default=Level.GREEN)
    debt = models.ForeignKey('parties.Debt', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField("O'qilgan", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bildirishnoma'
        verbose_name_plural = 'Bildirishnomalar'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_level_display()}] {self.title}'
