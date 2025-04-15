
# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message
# chat/views.py
from accounting.models import CustomUser  # Импортируем CustomUser вместо get_user_model
from userprofile.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@csrf_exempt
@login_required
def upload_message_file(request):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=request.POST.get('chat_id'))
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        if image and image.size > 1024 * 1024:
            return JsonResponse({'success': False, 'error': 'Изображение больше 1MB'})

        if file and (file.size > 10 * 1024 * 1024 or not file.name.endswith('.zip')):
            return JsonResponse({'success': False, 'error': 'ZIP-файл должен быть меньше 10MB'})

        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            image=image if image else None,
            file=file if file else None
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat.id}',
            {
                'type': 'chat_message',
                'sender_id': request.user.id,
                'image_url': message.image.url if message.image else None,
                'file_url': message.file.url if message.file else None,
            }
        )

        # можешь отправить через WebSocket, например через Channel Layer
        return JsonResponse({'success': True})




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


