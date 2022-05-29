from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    id = models.AutoField(
        'id группы',
        primary_key=True,
    )
    title = models.CharField(
        help_text='Имя группы.',
        max_length=200,
    )
    slug = models.SlugField(
        help_text='Адрес группы',
        unique=True,
    )
    description = models.TextField(
        help_text='Описание группы',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группа'

    def __str__(self):
        return self.title


class Post(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    text = models.TextField(
        help_text='Текст поста.',
    )
    pub_date = models.DateTimeField(
        help_text='Дата публикации поста.',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        to=User,
        help_text='Автор поста',
        related_name='posts',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        to=Group,
        help_text='Группа к которой относится пост.',
        related_name='posts',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
