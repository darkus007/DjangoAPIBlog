from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Post


class PostTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create_user(username='test_user', password='abc123')
        cls.test_post = Post.objects.create(author=cls.test_user, title='Blog title', body='Body content...')

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        author = f'{post.author}'
        title = f'{post.title}'
        body = f'{post.body}'
        self.assertEqual(author, 'test_user')
        self.assertEqual(title, 'Blog title')
        self.assertEqual(body, 'Body content...')

    def test_auto_time_created(self):
        """
        Проверка автозаполнения поля time_created
        и его принадлежность классу datetime.
        """
        self.assertTrue(isinstance(self.test_post.created_at, datetime))

    def test_str(self):
        self.assertEqual(f'{self.test_post.title} - {self.test_post.author}', self.test_post.__str__())
