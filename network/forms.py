from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField

from .models import *


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    error_messages = {
        'Пароли не совпадают'
    }

    class Meta:
        model = Profile
        fields = ['email', 'username', 'snusoman', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'snusoman': forms.Select(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    username = UsernameField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['email', 'password']


class ProfileChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['snusoman'].empty_label = 'Снюсоед не выбран'

    class Meta:
        model = Profile
        fields = ['nickname', 'slug', 'snusoman', 'profile_pic', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'snusoman': forms.Select(attrs={'class': 'form-control'}),
        }


class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': '10', 'style': 'resize:none;', 'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 3, 'style': 'resize:none;'})
        }
