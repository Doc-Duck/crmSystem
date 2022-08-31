from django.urls import path, include
from .views import *


urlpatterns = [
    path('', main, name='main'),
    path('complete/<todo_id>', completeTodo, name='complete'),
    path('delete/', delete_all_completed, name='delete_all'),
    path('delete_one/<todo_id>', delete_one, name='delete_one'),
    path('settings/', settings, name='settings'),
    path('sales/', sales, name='sales'),
    path('add_client/', add_client, name='add_client'),
    path('add_deal/', add_deal, name='add_deal'),
    path('products/', products, name='products'),
    path('products_add/', prod_add_form, name='products_add'),
    path('department/', department_managment, name='department')
]