# Buxgalteriya Boshqaruv Tizimi (Django)

Kichik/o'rta biznes uchun to'liq buxgalteriya tizimi: daromad-xarajat, debitor/kreditor
qarzdorlik (avtomatik eslatmalar bilan), valyuta kurslari (Markaziy bank), xodimlar,
soliqlar, ombor, hujjatlar (PDF), hisobotlar (Excel), rollar bo'yicha ruxsatlar va audit jurnali.

## 1. Talablar
- Python 3.11+
- Supabase'da yaratilgan PostgreSQL baza (bepul reja yetarli)
- Render.com akkaunt (bepul/starter reja)

## 2. Supabase bazasini sozlash
1. https://supabase.com -> New Project yarating.
2. Project Settings -> Database -> Connection string (yoki Connection info) bo'limidan
   quyidagilarni oling: Host, Database name, User, Password, Port.
   **Muhim:** "Connection pooling" (Session yoki Transaction mode, port 5432/6543) manzilini oling,
   Render kabi tashqi serverlar uchun shu tavsiya etiladi.
3. Bu qiymatlarni keyinroq Render'dagi Environment Variables'ga kiritasiz.

## 3. Lokal test qilish (ixtiyoriy)
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # va .env faylini o'z ma'lumotlaringiz bilan to'ldiring
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Brauzerda: http://127.0.0.1:8000/ (sayt) va http://127.0.0.1:8000/admin/ (boshqaruv paneli)

## 4. Render'ga 24/7 joylashtirish
### A) GitHub orqali (tavsiya etiladi)
1. Ushbu loyihani GitHub'ga yuklang (`git init && git add . && git commit -m "init" && git push`).
2. Render.com -> New -> **Blueprint** -> GitHub repo'ni tanlang (`render.yaml` avtomatik topiladi).
3. So'ralganda Supabase ma'lumotlarini kiriting: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`.
4. Deploy tugmasini bosing. Render avtomatik ravishda:
   - web-server (sayt),
   - `qarz-eslatmalari` cron job (har kuni qarz muddatlarini tekshiradi),
   - `valyuta-kurslari` cron job (har kuni Markaziy bank kursini yangilaydi)
   larni yaratadi.
5. Birinchi marta admin foydalanuvchi yaratish uchun Render Dashboard -> Shell bo'limidan:
   ```bash
   python manage.py createsuperuser
   ```

### B) Qo'lda (Blueprint ishlatmasdan)
1. Render -> New -> Web Service -> repo'ni ulang.
2. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
3. Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
4. Environment -> quyidagi o'zgaruvchilarni qo'shing (`.env.example` ga qarang):
   `SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SSLMODE`
5. Deploy bo'lgach, Shell orqali: `python manage.py migrate` va `python manage.py createsuperuser`
6. Cron ishlarni qo'lda yaratish uchun: Render -> New -> Cron Job, xuddi yuqoridagi
   `render.yaml` dagi kabi Command va Schedule kiriting.

## 5. Birinchi sozlash (admin sifatida kirgach)
1. `/admin/` ga kiring -> **Foydalanuvchilar** bo'limidan xodimlarga login yarating,
   har biriga mos **rol** bering (Direktor, Buxgalter, Menejer, Auditor).
2. **Kompaniya sozlamalari** (core ilovasi) bo'limida kompaniya nomi, logotip,
   QQS va foyda solig'i stavkalarini kiriting.
3. **Kategoriyalar** (Daromad/Xarajat) qo'shing.
4. Kontragentlar (mijoz/yetkazib beruvchi) qo'shing, so'ng qarzdorliklarni kiriting.

## 6. Rollar va huquqlar
| Rol | Huquqi |
|---|---|
| Super Admin | Barcha bo'limlarga to'liq kirish |
| Direktor | Barcha bo'limlarni ko'rish va tahrirlash |
| Buxgalter | Moliyaviy amaliyotlarni kiritish/tahrirlash |
| Menejer | Kontragent va qarzdorlik bilan ishlash |
| Auditor | Faqat ko'rish (yozish/o'chirish taqiqlangan) |

Django admin panelida esa standart Django `Group`/`Permission` tizimi orqali
har bir foydalanuvchiga qaysi modellarga ruxsat borligini yanada nozik sozlash mumkin
(Foydalanuvchi tahrirlash sahifasida "Permissions" bo'limi).

## 7. Avtomatik eslatmalar qanday ishlaydi
`send_debt_reminders` buyrug'i (cron orqali har kuni) barcha faol qarzdorliklarni tekshiradi:
30, 15, 7, 3, 1 kun qolganda va muddat kunida hamda muddati o'tganda bildirishnoma yaratadi.
Bu bildirishnomalar sahifa yuqorisida rangli banner (🔴🟠🟡) sifatida va "Bildirishnomalar"
bo'limida ko'rinadi. Foydalanuvchi brauzer push'ga ruxsat bergan bo'lsa, brauzer bildirishnomasi
ham chiqadi.

## 8. Zaxira nusxa (backup)
Supabase avtomatik kunlik backup beradi (Project Settings -> Database -> Backups).
Qo'shimcha xavfsizlik uchun: `pg_dump` orqali qo'lda export qilishingiz ham mumkin.

## 9. Loyihaning tuzilishi
```
config/        - global sozlamalar, URL marshrutlari
accounts/      - foydalanuvchilar, rollar, audit jurnali, JWT
core/          - dashboard, kompaniya sozlamalari
finance/       - daromad/xarajat
parties/       - mijoz/yetkazib beruvchi, debitor/kreditor qarzdorlik
currency/      - Markaziy bank valyuta kurslari
hr/            - xodimlar, maosh/bonus/jarima/avans
taxes/         - soliqlar, soliq kalendari
warehouse/     - mahsulotlar, kirim/chiqim
documents/     - hisob-faktura, shartnoma, PDF
reports/       - kunlik/haftalik/oylik/yillik hisobot, Excel eksport
notifications/ - rangli bildirishnomalar, avtomatik eslatma komandasi
templates/     - barcha HTML shablonlar (Bootstrap 5 asosida)
```
