# accounting/urls.py
from django.urls import path
from .views import register_view, login_view, show_home, show_profile

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('home/', show_home, name='home'),
    path('profile/', show_profile, name='profile'),
]
