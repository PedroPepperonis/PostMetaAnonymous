# Generated by Django 3.2.2 on 2021-05-25 08:36

from django.conf import settings
from django.db import migrations, models
import network.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('network', '0016_auto_20210525_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=30, null=True, validators=[network.models.validate_nickname], verbose_name='Позывной'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким логином уже сущесвует'}, max_length=30, null=True, unique=True, verbose_name='Логин'),
        ),
    ]
