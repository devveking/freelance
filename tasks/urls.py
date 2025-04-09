# tasks/urls.py
from django.urls import path


from .views import create_task, task_detail, edit_task, delete_task, archive_task

urlpatterns = [
    path('create/', create_task, name='create_task'),

    path('job/<int:id>/', task_detail, name='task_detail'),

    path('task/<int:id>/edit/', edit_task, name='edit_task'),
    path('task/<int:id>/delete/', delete_task, name='delete_task'),
    path('task/<int:id>/archive/', archive_task, name='archive_task'),
]