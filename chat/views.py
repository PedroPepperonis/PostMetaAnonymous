from django.shortcuts import render


def index(request):
    return render(request, 'PostMetaAnonymous/chat/index.html', context={})


def room(request, room_name):
    return render(request, 'PostMetaAnonymous/chat/room.html', {'room_name': room_name})
