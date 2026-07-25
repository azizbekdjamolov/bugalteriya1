from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.transaction_list, name='list'),
    path('yangi/', views.transaction_create, name='create'),
    path('<int:pk>/tahrirlash/', views.transaction_update, name='update'),
    path('<int:pk>/ochirish/', views.transaction_delete, name='delete'),
    path('kategoriyalar/', views.category_list, name='categories'),
]
