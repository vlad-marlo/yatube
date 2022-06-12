from math import ceil

from django import forms
from django.conf import settings as s
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, Follow

User = get_user_model()


class PostViewTest(TestCase):
    def setUp(self):
        self.small_image = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile(
            name='small.png',
            content=self.small_image,
            content_type='image/png'
        )
        self.user = User.objects.create_user(
            username='test_user'
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.second_user = User.objects.create_user(
            username='second_test_user'
        )
        self.second_client = Client()
        self.second_client.force_login(self.second_user)
        self.group = Group.objects.create(
            slug='test_group',
            description='test group description',
            title='test group title'
        )
        self.post = Post.objects.create(
            author=self.user,
            text='first_ post text',
            group=self.group,
            image=self.uploaded
        )
        self.second_post = Post.objects.create(
            author=self.user,
            text='test post text',
            group=self.group,
        )
        self.second_group = Group.objects.create(
            slug='second_test_group',
            description='second test group description',
            title='second test group title'
        )
        self.third_post = Post.objects.create(
            author=self.user,
            text='third test post text',
            group=None,
        )
        self.fourth_post = Post.objects.create(
            author=self.second_user,
            text='fourth test post text',
            group=None,
        )
        Follow.objects.create(user=self.second_user, author=self.user)
        cache.clear()

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug
            }): 'posts/group_list.html',
            reverse('posts:profile', kwargs={
                'username': self.user.username
            }): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.id
            }): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.id
            }): 'posts/post_create.html',
            reverse('posts:follow_index'): 'posts/follow.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        response = self.client.get(reverse('posts:index'))
        list_of_posts = [
            self.post,
            self.second_post,
            self.third_post,
            self.fourth_post,
        ]
        for post in list_of_posts:
            with self.subTest(post=post):
                self.assertIn(post, response.context['page_obj'])
        self.assertEqual(
            len(response.context['page_obj']),
            len(list_of_posts)
        )
        self.assertIsNotNone(response.context['page_obj'][0].image)

    def test_group_page_show_correct_context(self):
        response = self.client.get(
            reverse(
                'posts:group_list', kwargs={
                    'slug': self.group.slug,
                }
            )
        )
        list_of_correct_posts = [
            self.post,
            self.second_post,
        ]
        list_of_not_groups_posts = [
            self.third_post,
            self.fourth_post,
        ]
        for post in list_of_correct_posts:
            with self.subTest(post=post):
                self.assertIn(post, response.context['page_obj'])
        for post in list_of_not_groups_posts:
            with self.subTest(post=post):
                self.assertNotIn(post, response.context['page_obj'])
        self.assertEqual(response.context['group'], self.group)
        self.assertEqual(
            len(response.context['page_obj']),
            len(list_of_correct_posts),
        )
        self.assertIsNotNone(response.context['page_obj'][0].image)

    def test_profile_page_show_correct_context(self):
        response = self.client.get(
            reverse(
                'posts:profile', kwargs={
                    'username': self.user.username
                }
            )
        )
        test_user_posts = [
            self.post,
            self.second_post,
            self.third_post,
        ]
        for post in test_user_posts:
            with self.subTest(post=post):
                self.assertIn(post, response.context['page_obj'])
        self.assertEqual(response.context['author'], self.user)

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={
                    'post_id': self.post.id,
                }
            )
        )
        correct_context_data = {
            'post': self.post,
            'title': self.post.text[:30],
            'count': self.post.author.posts.count(),
        }
        for field, value in correct_context_data.items():
            with self.subTest(field=field):
                self.assertEqual(response.context[field], value)
        self.assertIsInstance(
            response.context['form'].fields['text'],
            forms.fields.CharField
        )
        self.assertIsNotNone(response.context['post'].image)

    def test_create_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_cache(self):
        response = self.client.get(reverse('posts:index'))
        Post.objects.filter(id=self.post.id).delete()
        self.assertIn(
            self.post.text,
            response.content.decode('utf-8')
        )
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        self.assertNotIn(
            self.post.text,
            response.content.decode('utf-8')
        )

    def test_follow_index(self):
        response = self.second_client.get(reverse('posts:follow_index'))
        response_another_user = self.authorized_client.get(
            reverse('posts:follow_index')
        )
        posts_in = {
            self.post: True,
            self.second_post: True,
            self.third_post: True,
            self.fourth_post: False
        }
        for post, status in posts_in.items():
            with self.subTest(post=post):
                if posts_in[post]:
                    self.assertIn(post, response.context['page_obj'])
                else:
                    self.assertNotIn(post, response.context['page_obj'])
                self.assertNotIn(
                    post,
                    response_another_user.context['page_obj']
                )

    def test_follow_link(self):
        Follow.objects.filter(author=self.second_user, user=self.user).delete()
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={
                    'username': self.second_user.username,
                }
            )
        )
        self.assertTrue(
            Follow.objects.filter(
                author=self.second_user,
                user=self.user
            ).exists()
        )

    def test_unfollow_link(self):
        Follow.objects.get_or_create(author=self.second_user, user=self.user)
        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={
                    'username': self.second_user.username
                }
            )
        )
        self.assertFalse(
            Follow.objects.filter(
                author=self.second_user,
                user=self.user
            ).exists()
        )


class PaginatorViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.group = Group.objects.create(
            slug='test_group',
            description='test group description',
            title='test group title'
        )
        for _ in range(13):
            Post.objects.create(
                author=self.user,
                text='test post text(Да, фантазия у меня есть)',
                group=self.group,
            )
        self.last_page = ceil(Post.objects.count() / s.OBJECTS_PER_PAGE)
        self.objects_last_page = Post.objects.count() % s.OBJECTS_PER_PAGE
        cache.clear()

    def test_homepage_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), s.OBJECTS_PER_PAGE)

    def test_homepage_last_page_contains_correct_records(self):
        response = self.client.get(
            reverse('posts:index') + f'?page={self.last_page}'
        )
        self.assertEqual(
            len(response.context['page_obj']),
            self.objects_last_page
        )

    def test_group_page_first_page_contains_ten_records(self):
        response = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={
                    'slug': self.group.slug,
                },
            )
        )
        self.assertEqual(len(response.context['page_obj']), s.OBJECTS_PER_PAGE)

    def test_group_page_second_page_contains_correct_count_of_records(self):
        response = self.client.get(
            reverse(
                'posts:group_list', kwargs={
                    'slug': self.group.slug
                }
            ) + f'?page={self.last_page}'
        )
        self.assertEqual(
            len(response.context['page_obj']),
            self.objects_last_page
        )
