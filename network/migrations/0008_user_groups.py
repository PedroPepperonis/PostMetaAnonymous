# Generated by Django 3.2.2 on 2021-07-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, to='network.Group', verbose_name='Подписки'),
        ),
    ]
