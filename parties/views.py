from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import readonly_block
from .forms import DebtForm, DebtFilterForm, PartyForm
from .models import Debt, Party


@login_required
def debt_list(request):
    qs = Debt.objects.select_related('party').all()
    form = DebtFilterForm(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data
        if data.get('direction'):
            qs = qs.filter(direction=data['direction'])
        if data.get('status'):
            qs = qs.filter(status=data['status'])
        if data.get('currency'):
            qs = qs.filter(currency=data['currency'])
        if data.get('q'):
            qs = qs.filter(party__name__icontains=data['q'])

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'parties/debt_list.html', {'page_obj': page_obj, 'filter_form': form})


@login_required
def debt_create(request):
    if readonly_block(request):
        messages.error(request, "Sizda faqat ko'rish huquqi bor.")
        return redirect('parties:debt_list')
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, "Qarzdorlik qo'shildi.")
            return redirect('parties:debt_list')
    else:
        form = DebtForm()
    return render(request, 'parties/debt_form.html', {'form': form, 'title': 'Yangi qarzdorlik'})


@login_required
def debt_update(request, pk):
    if readonly_block(request):
        messages.error(request, "Sizda faqat ko'rish huquqi bor.")
        return redirect('parties:debt_list')
    obj = get_object_or_404(Debt, pk=pk)
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Qarzdorlik yangilandi.')
            return redirect('parties:debt_list')
    else:
        form = DebtForm(instance=obj)
    return render(request, 'parties/debt_form.html', {'form': form, 'title': 'Tahrirlash'})


@login_required
def debt_delete(request, pk):
    if readonly_block(request):
        messages.error(request, "Sizda faqat ko'rish huquqi bor.")
        return redirect('parties:debt_list')
    obj = get_object_or_404(Debt, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Qarzdorlik o'chirildi.")
        return redirect('parties:debt_list')
    return render(request, 'parties/debt_confirm_delete.html', {'object': obj})


@login_required
def party_list(request):
    parties = Party.objects.all()
    if request.method == 'POST':
        if readonly_block(request):
            messages.error(request, "Sizda faqat ko'rish huquqi bor.")
            return redirect('parties:party_list')
        form = PartyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kontragent qo'shildi.")
            return redirect('parties:party_list')
    else:
        form = PartyForm()
    return render(request, 'parties/party_list.html', {'parties': parties, 'form': form})
