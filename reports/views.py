from datetime import date, timedelta

import openpyxl
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render

from finance.models import Transaction
from parties.models import Debt

PERIODS = {
    'daily': 1,
    'weekly': 7,
    'monthly': 30,
    'yearly': 365,
}


def _get_range(period):
    days = PERIODS.get(period, 30)
    end = date.today()
    start = end - timedelta(days=days)
    return start, end


@login_required
def report_summary(request):
    period = request.GET.get('period', 'monthly')
    start, end = _get_range(period)

    qs = Transaction.objects.filter(date__gte=start, date__lte=end)
    income = qs.filter(type=Transaction.Type.INCOME).aggregate(s=Sum('amount'))['s'] or 0
    expense = qs.filter(type=Transaction.Type.EXPENSE).aggregate(s=Sum('amount'))['s'] or 0

    by_category = qs.values('category__name', 'type').annotate(total=Sum('amount')).order_by('-total')

    debitor_total = Debt.objects.filter(direction=Debt.Direction.DEBITOR).exclude(status=Debt.Status.CLOSED)
    kreditor_total = Debt.objects.filter(direction=Debt.Direction.KREDITOR).exclude(status=Debt.Status.CLOSED)

    context = {
        'period': period,
        'start': start,
        'end': end,
        'income': income,
        'expense': expense,
        'net': income - expense,
        'by_category': by_category,
        'debitor_count': debitor_total.count(),
        'kreditor_count': kreditor_total.count(),
    }
    return render(request, 'reports/summary.html', context)


@login_required
def export_excel(request):
    period = request.GET.get('period', 'monthly')
    start, end = _get_range(period)
    qs = Transaction.objects.filter(date__gte=start, date__lte=end).select_related('category')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Hisobot'
    ws.append(['Sana', 'Turi', 'Kategoriya', 'Summa', 'Valyuta', 'Izoh'])
    for t in qs:
        ws.append([str(t.date), t.get_type_display(), t.category.name, float(t.amount), t.currency, t.description])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="hisobot-{period}.xlsx"'
    wb.save(response)
    return response


@login_required
def export_debts_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Qarzdorlik'
    ws.append(['Kontragent', "Yo'nalishi", 'Summa', 'Valyuta', "To'langan", 'Qolgan', 'Muddat', 'Holati'])
    for d in Debt.objects.select_related('party').all():
        ws.append([d.party.name, d.get_direction_display(), float(d.amount), d.currency,
                   float(d.paid_amount), float(d.remaining_amount), str(d.due_date), d.get_status_display()])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="qarzdorlik.xlsx"'
    wb.save(response)
    return response
