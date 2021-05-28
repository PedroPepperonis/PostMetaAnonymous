# Generated by Django 3.2.2 on 2021-05-16 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20210515_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='snusoman',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='network.snusoman', verbose_name='Какой вы снюсоед?'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.profile', verbose_name='Автор'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000, null=True, verbose_name='Комментарий')),
                ('time_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата написания')),
                ('time_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='network.profile', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-time_create'],
            },
        ),
        migrations.AddField(
            model_name='thread',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='network.comment', verbose_name='Комментарий'),
        ),
    ]