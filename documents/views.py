from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from core.models import CompanySettings
from .models import Invoice


@login_required
def invoice_list(request):
    invoices = Invoice.objects.select_related('party').all()
    return render(request, 'documents/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    company = CompanySettings.get_solo()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="hisob-faktura-{invoice.number}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont('Helvetica-Bold', 16)
    p.drawString(20 * mm, height - 25 * mm, company.name)

    p.setFont('Helvetica-Bold', 14)
    p.drawString(20 * mm, height - 40 * mm, f'HISOB-FAKTURA № {invoice.number}')

    p.setFont('Helvetica', 11)
    y = height - 55 * mm
    lines = [
        f'Sana: {invoice.date}',
        f'Kontragent: {invoice.party.name}',
        f'Summa: {invoice.amount:,.2f} {invoice.currency}',
        f'Tavsif: {invoice.description or "-"}',
    ]
    for line in lines:
        p.drawString(20 * mm, y, line)
        y -= 8 * mm

    p.showPage()
    p.save()
    return response
