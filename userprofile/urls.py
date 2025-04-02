# accounting/urls.py
from django.urls import path
from .views import show_profile, edit_profile

urlpatterns = [
    path('user/<str:username>/', show_profile, name='user'),
    path("edit/", edit_profile, name="edit_profile"),
]
