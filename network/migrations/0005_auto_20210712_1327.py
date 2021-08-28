# Generated by Django 3.2.2 on 2021-07-12 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20210712_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='post',
            name='moderator',
        ),
        migrations.AddField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Администратор', to='network.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='moderator',
            field=models.ManyToManyField(blank=True, related_name='group_moderator', to=settings.AUTH_USER_MODEL),
        ),
    ]
