from django.urls import path
from . import views

app_name = 'parties'

urlpatterns = [
    path('qarzdorlik/', views.debt_list, name='debt_list'),
    path('qarzdorlik/yangi/', views.debt_create, name='debt_create'),
    path('qarzdorlik/<int:pk>/tahrirlash/', views.debt_update, name='debt_update'),
    path('qarzdorlik/<int:pk>/ochirish/', views.debt_delete, name='debt_delete'),
    path('', views.party_list, name='party_list'),
]
