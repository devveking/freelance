# tasks/urls.py
from django.urls import path


from .views import create_task, task_detail

urlpatterns = [
    path('create/', create_task, name='create_task'),

    path('job/<int:id>/', task_detail, name='task_detail'),
]