# Generated by Django 3.2.2 on 2021-09-01 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_auto_20210901_2044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['time_create'], 'verbose_name': 'Чат', 'verbose_name_plural': 'Чаты'},
        ),
        migrations.AlterModelOptions(
            name='messagebody',
            options={'ordering': ['time_send'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.RemoveField(
            model_name='chat',
            name='users',
        ),
        migrations.AddField(
            model_name='chat',
            name='user1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='first_user', to='network.user', verbose_name='Человек'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chat',
            name='user2',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='second_user', to='network.user', verbose_name='Человек'),
            preserve_default=False,
        ),
    ]