# Generated by Django 2.2.19 on 2021-11-20 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.CharField(max_length=50),
        ),
    ]