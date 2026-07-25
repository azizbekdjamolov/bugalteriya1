"""
O'zbekiston Markaziy banki (cbu.uz) rasmiy API'sidan valyuta kurslarini oladi.
Har kuni ishga tushirish uchun (Render Cron Job yoki celery beat):
    python manage.py fetch_currency_rates
"""
import datetime
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from currency.models import ExchangeRate

CBU_API_URL = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
TRACKED_CODES = [c for c, _ in settings.CURRENCY_CHOICES if c != 'UZS']


class Command(BaseCommand):
    help = "Markaziy bankdan bugungi valyuta kurslarini yuklab oladi"

    def handle(self, *args, **options):
        try:
            response = requests.get(CBU_API_URL, timeout=15)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f'CBU API xatosi: {exc}'))
            return

        today = datetime.date.today()
        saved = 0
        for item in data:
            code = item.get('Ccy')
            if code not in TRACKED_CODES:
                continue
            rate = item.get('Rate')
            diff = item.get('Diff', 0)
            ExchangeRate.objects.update_or_create(
                currency_code=code,
                date=today,
                defaults={'rate': rate, 'diff': diff or 0},
            )
            saved += 1
        self.stdout.write(self.style.SUCCESS(f'{saved} ta valyuta kursi yangilandi ({today}).'))
