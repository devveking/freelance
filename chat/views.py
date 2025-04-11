
# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message
# chat/views.py
from accounting.models import CustomUser  # Импортируем CustomUser вместо get_user_model
from userprofile.models import UserProfile
from django.contrib.auth.decorators import login_required


@login_required
def chat_page(request, chat_id=None):
    chats = Chat.objects.filter(participants=request.user)
    active_chat = None

    user_profile = get_object_or_404(UserProfile, user=request.user)

    if chat_id:
        active_chat = get_object_or_404(Chat, id=chat_id)
        if request.user not in active_chat.participants.all():
            return redirect('chat_page')

    return render(request, 'chat/chat_page.html', {
        'chats': chats,
        'active_chat': active_chat,
        'user_profile': user_profile,
    })

@login_required
def open_chat(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)  # Используем CustomUser

    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)

    return redirect('chat_page_with_id', chat_id=chat.id)


