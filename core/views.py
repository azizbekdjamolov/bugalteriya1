import json
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render

from finance.models import Transaction
from parties.models import Debt
from currency.models import ExchangeRate


@login_required
def dashboard(request):
    today = date.today()

    todays_income = Transaction.objects.filter(type=Transaction.Type.INCOME, date=today).aggregate(s=Sum('amount'))['s'] or Decimal(0)
    todays_expense = Transaction.objects.filter(type=Transaction.Type.EXPENSE, date=today).aggregate(s=Sum('amount'))['s'] or Decimal(0)
    net_profit_today = todays_income - todays_expense

    debitor_total = _sum_remaining(
    Debt.objects.filter(
        direction=Debt.Direction.DEBITOR
    ).exclude(
        status=Debt.Status.CLOSED
    )
)

    kreditor_total = _sum_remaining(
        Debt.objects.filter(
            direction=Debt.Direction.KREDITOR
        ).exclude(
            status=Debt.Status.CLOSED
        )
    )
    upcoming_debts = Debt.objects.exclude(status=Debt.Status.CLOSED).filter(
        due_date__gte=today, due_date__lte=today + timedelta(days=7)
    ).order_by('due_date')[:10]

    overdue_debts = Debt.objects.exclude(status=Debt.Status.CLOSED).filter(due_date__lt=today).order_by('due_date')[:10]

    rates = ExchangeRate.objects.filter(date=ExchangeRate.latest_date()) if ExchangeRate.objects.exists() else []

    last_transactions = Transaction.objects.select_related('category', 'created_by').order_by('-date', '-id')[:10]

    # Oxirgi 14 kunlik daromad/xarajat grafigi uchun ma'lumot
    chart_labels = []
    chart_income = []
    chart_expense = []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        chart_labels.append(d.strftime('%d-%m'))
        chart_income.append(float(Transaction.objects.filter(type=Transaction.Type.INCOME, date=d).aggregate(s=Sum('amount'))['s'] or 0))
        chart_expense.append(float(Transaction.objects.filter(type=Transaction.Type.EXPENSE, date=d).aggregate(s=Sum('amount'))['s'] or 0))

    context = {
        'todays_income': todays_income,
        'todays_expense': todays_expense,
        'net_profit_today': net_profit_today,
        'debitor_total': debitor_total,
        'kreditor_total': kreditor_total,
        'upcoming_debts': upcoming_debts,
        'overdue_debts': overdue_debts,
        'rates': rates,
        'last_transactions': last_transactions,
        'chart_labels': json.dumps(chart_labels),
        'chart_income': json.dumps(chart_income),
        'chart_expense': json.dumps(chart_expense),
        'today': today,
    }
    return render(request, 'dashboard/dashboard.html', context)


def _sum_remaining(qs):
    total = Decimal(0)
    for debt in qs:
        total += debt.remaining_amount
    return total
