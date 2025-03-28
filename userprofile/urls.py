# accounting/urls.py
from django.urls import path
from .views import show_profile

urlpatterns = [
    path('user/<str:username>/', show_profile, name='user'),
]
