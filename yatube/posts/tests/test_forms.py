from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, Comment

User = get_user_model()


class PostFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            slug='form_test_group',
            description='form test group slug',
            title='form test group title',
        )
        self.second_user = User.objects.create_user(username='not_author')
        self.authorized_not_author = Client()
        self.authorized_not_author.force_login(self.second_user)
        self.post_text = 'post text'
        self.post_group = None
        self.post = Post.objects.create(
            author=self.user,
            text=self.post_text,
            group=self.post_group,
        )
        self.post_edited_not_author_text = 'new edited test post'
        self.post_creation_text = 'new test post'
        self.post_creation_group = self.group
        self.post_edited_by_author_text = 'edited test post'
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
        self.post_form_text = 'some text'
        self.comment_text = 'some comment text'
        self.second_comment_text = 'second comment text'

    def test_create_post(self):
        form_data = [
            {
                'text': self.post_creation_text,
                'group': self.post_creation_group.id,
            },
            {
                'text': self.post_form_text,
                'group': self.group.id,
                'image': self.uploaded,
            },
        ]
        for data in form_data:
            post_count = Post.objects.count()
            response = self.authorized_client.post(
                reverse('posts:post_create'),
                data=data,
                follow=True,
            )
            self.assertRedirects(
                response, reverse(
                    'posts:profile',
                    kwargs={
                        'username': self.user.username
                    }
                )
            )
            self.assertEqual(Post.objects.count(), post_count + 1)
            self.assertEqual(
                Post.objects.order_by('-id').all()[0].text,
                data.get('text')
            )
            self.assertEqual(
                Post.objects.order_by('-id').all()[0].group.id,
                data.get('group')
            )
            if self.post.image:
                self.assertEqual(
                    Post.objects.order_by('-id').all()[0].image,
                    self.post.image
                )

    def test_edit_post_not_author(self):
        form_data = {
            'text': self.post_edited_not_author_text,
            'group': self.group.id
        }
        response = self.authorized_not_author.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail',
                kwargs={
                    'post_id': self.post.id
                }
            )
        )
        self.post.refresh_from_db()
        check_data = {
            'text': self.post.text,
            'group': self.post.group,
        }
        expected_data = {
            self.post.text: self.post_text,
            self.post.group: self.post_group,
        }
        for field, value in check_data.items():
            with self.subTest(value=value):
                self.assertNotEqual(
                    value,
                    form_data[field]
                )
        for value, expected in expected_data.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value,
                    expected
                )

    def test_edit_post_author(self):
        form_data = {
            'text': self.post_edited_by_author_text,
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail',
                kwargs={
                    'post_id': self.post.id
                }
            )
        )
        self.post.refresh_from_db()
        value_and_expected = {
            self.post.text: form_data['text'],
            self.post.group.id: form_data['group'],
            self.post.author: self.user
        }
        for value, expected in value_and_expected.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_comment_form_authorized_user(self):
        data = {
            'text': self.comment_text,
        }
        count_comment = Comment.objects.count()
        self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': self.post.id}
            ),
            data=data,
            follow=True,
        )
        self.assertEqual(Comment.objects.count(), count_comment + 1)
        check_data = {
            self.post.comments.all()[0].text: data['text'],
            self.post.comments.all()[0].author.id: self.user.id,
            self.post.comments.all()[0].post.id: self.post.id
        }
        for field, expected in check_data.items():
            with self.subTest(field=field):
                self.assertEqual(field, expected)

    def test_comment_form_anonymous_user(self):
        data = {
            'text': self.second_comment_text,
        }
        count_comment = Comment.objects.filter(
            post_id=self.post.id
        ).count()
        self.client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': self.post.id}
            ),
            data=data,
            follow=True,
        )
        self.assertEqual(
            Comment.objects.filter(
                post_id=self.post.id
            ).count(),
            count_comment
        )
