# Generated by Django 3.2.2 on 2021-07-12 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210712_1319'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostGroup',
            new_name='Group',
        ),
    ]