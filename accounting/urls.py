# accounting/urls.py
from django.urls import path
from .views import register_view, login_view  # импорт login_view (новый)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]
