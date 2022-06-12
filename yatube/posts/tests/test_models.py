from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='auth')
        self.group_title = 'Тестовая группа'
        self.group_slug = 'test_slug'
        self.group_description = 'Тестовое описание'
        self.post_text = 'Тестовый пост..........'
        self.comment_text = 'Текст тестового поста'
        self.group = Group.objects.create(
            title=self.group_title,
            slug=self.group_slug,
            description=self.group_description,
        )
        self.post = Post.objects.create(
            author=self.user,
            text=self.post_text,
        )
        self.text_field_help_text = 'Введите текст поста'
        self.group_field_help_text = 'Группа к которой будет относиться пост'
        self.post_verbose_name = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = self.post
        group = self.group
        test_str = {
            post: self.post.text[:15],
            group: self.group.title,
        }
        for value, expected in test_str.items():
            with self.subTest(value=value):
                self.assertEqual(
                    str(value), expected
                )

    def test_models_have_correct_help_text(self):
        post = self.post
        post_help_text = {
            'text': self.text_field_help_text,
            'group': self.group_field_help_text,
        }
        for value, expected in post_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_models_have_correct_verbose_names(self):
        for value, expected in self.post_verbose_name.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).verbose_name,
                    expected
                )
