from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer


class Settings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        settings.SECRET_KEY = "some_secret_key!"

        cls.test_user = get_user_model().objects.create_user(username='test_user', password='abc123')
        cls.test_post = Post.objects.create(author=cls.test_user, title='Post title', body='Body content...')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        settings.SECRET_KEY = None


class PostSerializerTestCase(Settings):     # python manage.py test blog.tests.test_serializers.PostSerializerTestCase
    """ Тестируем PostSerializer. """
    def test_ok(self):
        data = PostSerializer(self.test_post).data
        expected_data = {'id': 1, 'author': 1, 'title': 'Post title', 'body': 'Body content...',
                         'created_at': self.test_post.created_at.isoformat().replace("+00:00", "Z")
                         }
        self.assertEqual(data, expected_data)


class UserSerializerTestCase(Settings):     # python manage.py test blog.tests.test_serializers.UserSerializerTestCase
    """ Тестируем PostSerializer. """
    def test_ok(self):
        data = UserSerializer(self.test_user).data
        expected_data = {'id': 1, 'username': 'test_user'}
        self.assertEqual(data, expected_data)
