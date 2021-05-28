# Generated by Django 3.2.2 on 2021-05-19 07:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('network', '0014_profile_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='Логин'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(error_messages={'unique': 'Анонимный пользователь с таким логином уже существует'}, max_length=30, null=True, verbose_name='Позывной'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(error_messages={'unique': 'Уже существует'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
