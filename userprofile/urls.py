# userprofile/urls.py
from django.urls import path
from .views import show_profile, edit_profile, delete_portfolio, edit_portfolio

urlpatterns = [
    path('user/<str:username>/', show_profile, name='user'),
    path("edit/", edit_profile, name="edit_profile"),
    path('delete-portfolio/', delete_portfolio, name='delete_portfolio'),
    path('edit-portfolio/<int:portfolio_id>/', edit_portfolio, name='edit_portfolio'),


]
