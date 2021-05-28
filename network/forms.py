from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class RegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['username', 'password', 'snusoman']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'snusoman': forms.Select(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):

    class Meta:
        model = Profile
        fields = ['username', 'password']


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
            'content': forms.Textarea(attrs={'cols': 50, 'rows': '10', 'style': 'resize:none;'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 3, 'style': 'resize:none;'})
        }
