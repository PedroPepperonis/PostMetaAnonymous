from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from pytils.translit import slugify


def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError('Максимальный размер фото - 2мб')


class ProfileManager(BaseUserManager):
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


class Profile(AbstractBaseUser):
    username = models.CharField(max_length=30, verbose_name='Логин', unique=True)
    email = models.EmailField(max_length=30, verbose_name='Email', unique=True)
    nickname = models.CharField(max_length=30, verbose_name='Позывной', unique=False)
    slug = models.SlugField(max_length=20, unique=True, db_index=True, verbose_name='URL',
                            error_messages={'unique': 'Пользователь с такой же ссылкой на профиль уже существует'})
    about = models.TextField(max_length=500, verbose_name='О себе', blank=True)
    snusoman = models.ForeignKey('Snusoman', on_delete=models.PROTECT, verbose_name='Какой вы снюсоед?', blank=True, null=True)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE, verbose_name='Ранг', blank=True, null=True)
    experience = models.IntegerField(default=0, verbose_name='Опыт')
    friends = models.ManyToManyField('Profile', blank=True)
    profile_pic = models.ImageField(blank=True, verbose_name='Аватар', upload_to='images/profile_pic/',
                                    validators=[validate_image])
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        value = self.username
        self.slug = slugify(value)
        if not self.nickname:
            self.nickname = self.username
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class FriendRequest(models.Model):
    from_user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='to_user')


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
    likes = models.ManyToManyField(Profile, blank=True, related_name='thread_likes')

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
    likes = models.ManyToManyField(Profile, blank=True, related_name='comment_likes')

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
