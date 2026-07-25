from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
]
