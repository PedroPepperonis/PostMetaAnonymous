import random

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from pytils.translit import slugify
from ckeditor.fields import RichTextField
from string import ascii_lowercase


def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError('Максимальный размер фото - 2мб')


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not username:
            raise ValueError('Должен быть логин')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.snusoman_id = 1
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, verbose_name='Логин', unique=True)
    email = models.EmailField(max_length=30, verbose_name='Email', unique=True)
    nickname = models.CharField(max_length=30, verbose_name='Позывной', unique=False)
    slug = models.SlugField(max_length=20, unique=True, db_index=True, verbose_name='URL',
                            error_messages={'unique': 'Пользователь с такой же ссылкой на профиль уже существует'})
    about = models.TextField(max_length=500, verbose_name='О себе', blank=True)
    snusoman = models.ForeignKey('Snusoman', on_delete=models.PROTECT, verbose_name='Какой вы снюсоед?', blank=False,
                                 null=True)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE, verbose_name='Ранг', blank=True, null=True)
    groups = models.ManyToManyField('Group', blank=True, verbose_name='Подписки')
    friends = models.ManyToManyField('User', blank=True, verbose_name='Друзья')
    experience = models.IntegerField(default=0, verbose_name='Опыт')
    profile_pic = models.ImageField(blank=True, verbose_name='Аватар', upload_to='PostMetaAnonymousStorage/profile_pic/',
                                    validators=[validate_image])
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        if not self.nickname:
            self.nickname = self.username
        if not self.rank:
            self.rank_id = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class FriendRequest(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='От пользователя',
                                  related_name='friend_request_from_user')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='К пользователю',
                                related_name='friend_request_to_user')

    class Meta:
        verbose_name = 'Запросы в друзья'
        verbose_name_plural = 'Запросы в друзья'


class Snusoman(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Снюсоман')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Snusoman_URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['name']


class Group(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название сообщества')
    about = models.CharField(max_length=1000, verbose_name='Описание')
    group_avatar = models.ImageField(upload_to='PostMetaAnonymousStorage/profile_pic/', validators=[validate_image],
                                     verbose_name='Аватар сообщества', blank=True)
    background_photo = models.ImageField(validators=[validate_image], upload_to='PostMetaAnonymousStorage/profile_pic/',
                                         verbose_name='Фон сообщества', blank=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL сообщества')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    followers = models.ManyToManyField(User, blank=True, related_name='postgroup_followers', verbose_name='Подписчики')
    posts = models.ManyToManyField('Post', blank=True, related_name='postgroup_posts', verbose_name='Посты')
    admin = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Администратор', blank=False)
    moderator = models.ManyToManyField('User', blank=True, related_name='group_moderator', verbose_name='Модераторы')

    def __str__(self):
        return self.title

    def has_perm(self, perm, obj=None):
        return self.moderator

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ['title']


def create_unique_key(length):
    result = ''
    letters = ascii_lowercase
    for i in range(length):
        result += random.choice(letters)
    return result


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextField(blank=True, null=True, verbose_name='Текст')
    unique_id = models.CharField(max_length=6, unique=True, verbose_name='Уникальный id', null=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_important = models.BooleanField(default=False, verbose_name='Закрепить?')
    author = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Автор')
    likes = models.ManyToManyField('User', blank=True, related_name='post_likes')
    dislikes = models.ManyToManyField('User', blank=True, related_name='post_dislikes')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name='Сообщество')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        unique_id = create_unique_key(6)
        if not self.unique_id:
            self.unique_id = unique_id
        if not self.slug:
            value = f'{self.title}-{unique_id}'
            self.slug = slugify(value)
        super().save(*args, **kwargs)

    def get_likes_count(self):
        return self.likes.count()

    def get_dislikes_count(self):
        return self.dislikes.count()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-is_important', '-time_create']


class Comment(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1000, unique=False, verbose_name='Комментарий')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

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


class Rank(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Ранг')
    slug = models.SlugField(unique=True, verbose_name='URL')
    experience = models.IntegerField(verbose_name='Опыт')
    about = models.TextField(max_length=500, verbose_name='Описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ранг'
        verbose_name_plural = 'Ранги'
        ordering = ['experience']
