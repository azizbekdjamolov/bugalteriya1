from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404

from .models import Employee, SalaryRecord


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'hr/employee_list.html', {'employees': employees})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    records = employee.salary_records.all()
    totals = records.aggregate(
        bonus=Sum('amount', filter=Q(type=SalaryRecord.Type.BONUS)),
        penalty=Sum('amount', filter=Q(type=SalaryRecord.Type.PENALTY)),
        advance=Sum('amount', filter=Q(type=SalaryRecord.Type.ADVANCE)),
    )
    return render(request, 'hr/employee_detail.html', {'employee': employee, 'records': records, 'totals': totals})
