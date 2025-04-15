# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('<int:chat_id>/', views.chat_page, name='chat_page_with_id'),
    path('open/<int:user_id>/', views.open_chat, name='open_chat'),

    path('upload/', views.upload_message_file, name='upload_message_file'),

]
