# Generated by Django 2.2.6 on 2021-12-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20211218_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Текст нового поста', verbose_name='Текст поста'),
        ),
    ]
