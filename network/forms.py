from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from ckeditor.widgets import CKEditorWidget

from .models import User, Post, Comment, Group


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form_column__field', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form_column__field', 'placeholder': 'Подтвердите пароль'})
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'snusoman']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_column__field', 'placeholder': 'Логин'}),
            'email': forms.EmailInput(attrs={'class': 'form_column__field', 'placeholder': 'Почта'}),
            'snusoman': forms.Select(attrs={'class': 'form_column__select', 'placeholder': 'Какой вы снюсоед?'}),
        }


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form_column__field', 'placeholder': 'Пароль'})
    )
    username = UsernameField(widget=forms.EmailInput(attrs={'class': 'form_column__field' , 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['email', 'password']


class ProfileChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['snusoman'].empty_label = 'Снюсоед не выбран'

    class Meta:
        model = User
        fields = ['nickname', 'snusoman', 'profile_pic', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form_column__textarea'}),
            'nickname': forms.TextInput(attrs={'class': 'form_column__title'}),
            'profile_pic': forms.FileInput(attrs={}),
            'snusoman': forms.Select(attrs={'class': 'form_column__select'}),
        }


class PostForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        groups = Group.objects.filter(followers=user)
        self.fields['group'].queryset = groups
        self.fields['group'].empty_label = 'Выберите сообщество'

    class Meta:
        model = Post
        fields = ['group', 'title', 'content']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Заголовок', 'class': 'form_column__title', 'autocomplete': 'off'}),
            'group': forms.Select(attrs={'class': 'form_column__select'})
        }


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Заголовок', 'class': 'form_column__title', 'autocomplete': 'off'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'comment_content', 'placeholder': 'Оставьте комментарий'})
        }


class GroupAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(kwargs)
        group = Group.objects.get(slug=kwargs['instance'].slug)
        followers = group.followers.all()
        posts = group.posts.all()
        self.fields['followers'].queryset = followers
        self.fields['posts'].queryset = posts
        self.fields['moderator'].queryset = followers

    class Meta:
        model = Group
        fields = ['title', 'about', 'followers', 'posts', 'moderator', 'group_avatar', 'background_photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form_column__title', 'placeholder': 'Название сообщества'}),
            'about': forms.Textarea(attrs={'class': 'form_column__textarea', 'placeholder': 'Описание'}),
            'followers': forms.SelectMultiple(attrs={'class': 'form_column__select', 'placeholder': 'Подписчики'}),
            'posts': forms.SelectMultiple(attrs={'class': 'form_column__select', 'placeholder': 'Подписчики'}),
            'moderator': forms.SelectMultiple(attrs={'class': 'form_column__select', 'placeholder': 'Подписчики'}),
            'group_avatar': forms.FileInput(attrs={'class': '', 'placeholder': 'Аватар группы'}),
            'background_photo': forms.FileInput(attrs={'class': '', 'placeholder': 'Задний фон'}),
        }


class GroupModeratorForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['followers']
