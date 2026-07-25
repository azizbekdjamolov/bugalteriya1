"""
Har kuni ishga tushiriladigan buyruq: barcha faol qarzdorliklarni tekshirib,
muddatiga qarab (30, 15, 7, 3, 1, 0 kun va muddati o'tgan) bildirishnoma yaratadi.

Render'da "Cron Job" sifatida sozlang:
    Command: python manage.py send_debt_reminders
    Schedule: 0 4 * * *   (har kuni ertalab, Tashkent vaqti bilan taxminan 09:00)
"""
from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand

from notifications.models import Notification
from parties.models import Debt

LEVEL_BY_DAYS = {
    0: Notification.Level.RED,      # bugun
    1: Notification.Level.ORANGE,
    3: Notification.Level.YELLOW,
    7: Notification.Level.YELLOW,
    15: Notification.Level.YELLOW,
    30: Notification.Level.YELLOW,
}


class Command(BaseCommand):
    help = "Muddati yaqinlashayotgan/o'tgan qarzdorliklar bo'yicha bildirishnoma yaratadi"

    def handle(self, *args, **options):
        today = date.today()
        created = 0

        active_debts = Debt.objects.exclude(status=Debt.Status.CLOSED)

        for debt in active_debts:
            debt.refresh_status(save=True)
            days_left = debt.days_left

            if days_left < 0:
                level = Notification.Level.RED
                title = f'❗ Muddati o\'tgan: "{debt.party.name}"'
                message = (f'"{debt.party.name}" bilan bog\'liq {debt.get_direction_display().lower()} '
                            f'{debt.remaining_amount} {debt.currency} qarzining to\'lov muddati '
                            f'{abs(days_left)} kun oldin o\'tib ketgan.')
            elif days_left in settings.DEBT_REMINDER_DAYS:
                level = LEVEL_BY_DAYS.get(days_left, Notification.Level.YELLOW)
                if days_left == 0:
                    title = f'🔴 Bugun to\'lanishi kerak: "{debt.party.name}"'
                else:
                    title = f'⏰ {days_left} kun qoldi: "{debt.party.name}"'
                message = (f'"{debt.party.name}"ning {debt.remaining_amount} {debt.currency} '
                            f'{debt.get_direction_display().lower()} qarzi {days_left} kundan so\'ng '
                            f'({debt.due_date}) to\'lanishi kerak.')
            else:
                continue

            # bir xil kunda ikki marta bildirishnoma yaratmaslik uchun
            exists_today = Notification.objects.filter(
                debt=debt, created_at__date=today, title=title
            ).exists()
            if not exists_today:
                Notification.objects.create(title=title, message=message, level=level, debt=debt)
                created += 1

        self.stdout.write(self.style.SUCCESS(f'{created} ta yangi bildirishnoma yaratildi.'))
