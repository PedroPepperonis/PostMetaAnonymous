# Generated by Django 3.2.2 on 2021-08-21 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0020_remove_post_unique_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unique_key',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True, verbose_name='Уникальный id'),
        ),
    ]
