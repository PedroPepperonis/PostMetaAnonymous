# Generated by Django 3.2.2 on 2021-07-12 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_rename_postgroup_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='admin',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Администратор', to='network.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='moderator',
            field=models.ManyToManyField(blank=True, related_name='group_moderator', to=settings.AUTH_USER_MODEL),
        ),
    ]