from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Имя группы.',
        max_length=200,
    )
    slug = models.SlugField(
        'Адрес группы',
        unique=True,
    )
    description = models.TextField(
        'Описание группы',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группа'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста.',
    )
    pub_date = models.DateTimeField(
        'Дата публикации поста.',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        help_text='Автор поста',
        to=User,
        related_name='posts',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        help_text='Группа к которой относится пост.',
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
