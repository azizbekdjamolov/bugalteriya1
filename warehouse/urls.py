from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('', views.product_list, name='list'),
]
