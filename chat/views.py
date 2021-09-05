from django.shortcuts import render

from .models import Chat, User


def chat_index(request):
    return render(request, 'PostMetaAnonymous/Chat/chat.html', {})


def chat_room(request, username):
    other_user = User.objects.get(slug=username)
    chat = Chat.objects.get_or_create_chat(request.user, other_user)
    return render(request, 'PostMetaAnonymous/Chat/chat_room.html', {'chat_id': username, 'chat': chat,
                                                                     'other_user': other_user})
