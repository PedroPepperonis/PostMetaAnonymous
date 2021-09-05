from django.contrib import admin

from .models import Chat, MessageBody


class ChatAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'title', 'time_create')


class MessageBodyAdmin(admin.ModelAdmin):
    list_display = ('chat_fk', 'sender', 'receiver', 'content')


admin.site.register(Chat, ChatAdmin)
admin.site.register(MessageBody, MessageBodyAdmin)
