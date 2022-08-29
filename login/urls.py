from django.urls import path, include
from .views import index, registration, logout


urlpatterns = [
    path('', index),
    path('registration/', registration, name='reg'),
    path('', logout, name='logout')
]