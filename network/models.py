from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from pytils.translit import slugify


def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError('Максимальный размер фото - 2мб')


def validate_nickname(nickname):
    anonymous_name = ('anonymous', 'anonym', 'анонимус', 'аноним')

    for i in range(0, len(anonymous_name)):
        if nickname.lower().find(anonymous_name[i]) != -1:
            return 0
    raise ValidationError(f'В вашем позывном нет anonymous, anonym, анонимус, или аноним.')


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, error_messages={'unique': 'Уже существует'})
    snusoman = models.ForeignKey('Snusoman', on_delete=models.PROTECT, verbose_name='Какой вы снюсоед?', null=True)
    profile_pic = models.ImageField(null=True, blank=True, verbose_name='Аватар', upload_to='images/profile_pic/',
                                    validators=[validate_image])
    username = models.CharField(max_length=30, verbose_name='Логин', unique=True, null=True,
                                error_messages={'unique': 'Пользователь с таким логином уже сущесвует'})
    nickname = models.CharField(max_length=30, verbose_name='Позывной', unique=False, null=True,
                                validators=[validate_nickname])
    slug = models.SlugField(max_length=20, unique=True, db_index=True, verbose_name='URL',
                            error_messages={'unique': 'Пользователь с такой же ссылкой на профиль уже существует'})
    about = models.TextField(max_length=500, verbose_name='О себе', blank=True)
    password = models.CharField(max_length=32, verbose_name='Пароль', null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Snusoman(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Снюсоман')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Snusoman_URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['name']


class Thread(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.CharField(max_length=1000, verbose_name='Текст поста')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_important = models.BooleanField(default=False, verbose_name='Закрепить?')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор')
    likes = models.ManyToManyField(User, related_name='thread_likes')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def get_likes_count(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Тред'
        verbose_name_plural = 'Треды'
        ordering = ['-time_create']


class Comment(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1000, unique=False, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    replies = models.ForeignKey('Reply', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_likes_count(self):
        return self.likes.count()

    def get_likes(self):
        return self.likes

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']


class Reply(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)
    for_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=1000, unique=False, verbose_name='Ответ на комментарий', null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа', null=True)
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', null=True)
    likes = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Ответ на комментарий'
        verbose_name_plural = 'Ответы на комментарии'
        ordering = ['time_create']
