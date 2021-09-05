from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

from network.models import create_unique_key

User = get_user_model()


class ChatManager(models.Manager):
    def get_or_create_chat(self, user1, user2):
        chat = self.get_queryset().filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))\
            .distinct()
        if chat.exists():
            return chat[0]
        new_chat = self.create(
            unique_id=create_unique_key(6),
            user1=user1,
            user2=user2,
            title=f'Chat {user1} {user2}'
        )
        new_chat.save()
        return new_chat


class Chat(models.Model):
    unique_id = models.CharField(max_length=6, unique=True, verbose_name='Id чата')
    title = models.CharField(max_length=255, verbose_name='Название чата')
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user1',
                              verbose_name='Пользователи чата')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user2',
                              verbose_name='Пользователи чата')
    messages = models.ManyToManyField('MessageBody', blank=True, verbose_name='Сообщения')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания чата')

    objects = ChatManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['time_create']


class MessageBody(models.Model):
    chat_fk = models.ForeignKey('Chat', on_delete=models.CASCADE, verbose_name='Чат')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender',
                               verbose_name='Отправитель')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver',
                                 verbose_name='Получатель')
    content = models.TextField(max_length=10000, blank=False, unique=False, verbose_name='Сообщение')
    time_send = models.DateTimeField(auto_now_add=True, verbose_name='Время когда было отправлено сообщение')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['time_send']
