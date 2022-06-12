from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_author = User.objects.create_user(username='not_author')
        self.not_author_ = Client()
        self.not_author_.force_login(self.not_author)
        self.group = Group.objects.create(
            slug='test_group',
            description='test group description',
            title='test group title'
        )
        self.post = Post.objects.create(
            author=self.user,
            text='test post text(Да, фантазия у меня есть)',
            group=self.group,
        )

    def test_links_guest_client(self):
        urls = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user.username}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/edit/': HTTPStatus.FOUND,
            '/create/': HTTPStatus.FOUND,
            '/follow/': HTTPStatus.FOUND,
        }
        for url, status in urls.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_links_authorized_client(self):
        urls = [
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.id}/',
            f'/posts/{self.post.id}/edit/',
            '/create/',
            '/follow/',
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_author_cant_edit_post(self):
        response = self.not_author_.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_uses_correct_template(self):
        urls_uses_template = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/post_create.html',
            '/create/': 'posts/post_create.html',
            '/follow/': 'posts/follow.html',
        }
        for url, template in urls_uses_template.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
