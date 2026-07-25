from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import readonly_block
from .forms import TransactionForm, TransactionFilterForm, CategoryForm
from .models import Transaction, Category


@login_required
def transaction_list(request):
    qs = Transaction.objects.select_related('category', 'created_by').all()
    form = TransactionFilterForm(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data
        if data.get('q'):
            qs = qs.filter(description__icontains=data['q'])
        if data.get('type'):
            qs = qs.filter(type=data['type'])
        if data.get('category'):
            qs = qs.filter(category=data['category'])
        if data.get('date_from'):
            qs = qs.filter(date__gte=data['date_from'])
        if data.get('date_to'):
            qs = qs.filter(date__lte=data['date_to'])

    totals = qs.aggregate(
        income=Sum('amount', filter=Q(type=Transaction.Type.INCOME)),
        expense=Sum('amount', filter=Q(type=Transaction.Type.EXPENSE)),
    )

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'finance/transaction_list.html', {
        'page_obj': page_obj,
        'filter_form': form,
        'totals': totals,
    })


@login_required
def transaction_create(request):
    if readonly_block(request):
        messages.error(request, "Sizda faqat ko'rish huquqi bor.")
        return redirect('finance:list')
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            messages.success(request, "Operatsiya muvaffaqiyatli qo'shildi.")
            return redirect('finance:list')
    else:
        form = TransactionForm()
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': "Yangi operatsiya"})


@login_required
def transaction_update(request, pk):
    if readonly_block(request):
        messages.error(request, "Sizda faqat ko'rish huquqi bor.")
        return redirect('finance:list')
    obj = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operatsiya yangilandi.')
            return redirect('finance:list')
    else:
        form = TransactionForm(instance=obj)
    return render(request, 'finance/transaction_form.html', {'form': form, 'title': 'Tahrirlash'})


@login_required
def transaction_delete(request, pk):
    if readonly_block(request):
        messages.error(request, "Sizda faqat ko'rish huquqi bor.")
        return redirect('finance:list')
    obj = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Operatsiya o'chirildi.")
        return redirect('finance:list')
    return render(request, 'finance/transaction_confirm_delete.html', {'object': obj})


@login_required
def category_list(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        if readonly_block(request):
            messages.error(request, "Sizda faqat ko'rish huquqi bor.")
            return redirect('finance:categories')
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya qo'shildi.")
            return redirect('finance:categories')
    else:
        form = CategoryForm()
    return render(request, 'finance/category_list.html', {'categories': categories, 'form': form})
