from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_summary, name='summary'),
    path('excel/', views.export_excel, name='export_excel'),
    path('qarzdorlik/excel/', views.export_debts_excel, name='export_debts_excel'),
]
