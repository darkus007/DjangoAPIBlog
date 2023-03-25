"""
Тестируем PostViewSet и UserViewSet.

Так как используем ViewSet, проверяем только логику работы
классов доступа, которые были написаны для данного проекта
IsAuthorOrReadOnly и IsStaffOrReadOnly.

Проверяем предоставление обязательных полей.
"""

import logging

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.db.models import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer


class Settings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        settings.SECRET_KEY = "some_secret_key!"

        cls.test_user = get_user_model().objects.create_user(username='test_user', password='abc123')
        cls.test_user2 = get_user_model().objects.create_user(username='test_user_2', password='abc1234')
        cls.admin = get_user_model().objects.create_superuser(username='admin', password='admin_password')

        cls.test_post = Post.objects.create(author=cls.test_user, title='Post title', body='Body content...')

        cls.client = Client()
        cls.auth_client = Client()
        cls.not_author = Client()
        cls.admin_client = Client()

        cls.auth_client.force_login(cls.test_user)
        cls.not_author.force_login(cls.test_user2)
        cls.admin_client.force_login(cls.admin)

        logging.getLogger('django.request').setLevel(logging.ERROR)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        settings.SECRET_KEY = None


class PostViewSetTestCase(Settings):  # python manage.py test blog.tests.test_views.PostViewSetTestCase

    def test_api_get_many_posts_unauth(self):
        response = self.client.get('/api/v1/')
        serializer = PostSerializer([self.test_post], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_many_posts_auth(self):
        response = self.auth_client.get('/api/v1/')
        serializer = PostSerializer([self.test_post], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_many_posts_invalid_request(self):
        response = self.client.get('/aip/v1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_get_one_post_unauth(self):
        response = self.client.get('/api/v1/1/')
        serializer = PostSerializer(self.test_post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_one_post_auth(self):
        response = self.auth_client.get('/api/v1/1/')
        serializer = PostSerializer(self.test_post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_one_post_invalid_request(self):
        response = self.client.get('/api/v1/100/')
        expected_data = {'detail': ErrorDetail(string='Страница не найдена.', code='not_found')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_add_post_unauth(self):
        response = self.client.post('/api/v1/', data={'author': 1, 'title': 'Some', 'body': 'Some too'},
                                    content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='Учетные данные не были предоставлены.',
                                               code='not_authenticated')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_add_post_auth(self):
        response = self.auth_client.post('/api/v1/', data={'author': 1, 'title': 'Some', 'body': 'Some too'},
                                         content_type='application/json')
        added_post = Post.objects.get(pk=response.data['id'])
        serializer = PostSerializer(added_post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_patch_post_unauth(self):
        response = self.client.patch('/api/v1/1/', data={'title': 'Post title mod', 'body': 'Body content...'},
                                     content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='Учетные данные не были предоставлены.',
                                               code='not_authenticated')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_post_not_author(self):
        response = self.not_author.patch('/api/v1/1/', data={'title': 'Post title mod', 'body': 'Body content...'},
                                         content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                               code='permission_denied')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_post_admin(self):
        response = self.admin_client.patch('/api/v1/1/', data={'title': 'Post title mod', 'body': 'Body content...'},
                                           content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                               code='permission_denied')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_post_author(self):
        response = self.auth_client.patch('/api/v1/1/',
                                          data={'title': 'Post title mod', 'body': 'Body content...'},
                                          content_type='application/json')
        modified_post = Post.objects.get(pk=1)
        serializer = PostSerializer(modified_post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_delete_post_unauth(self):
        response = self.client.delete('/api/v1/1/')
        expected_data = {'detail': ErrorDetail(string='Учетные данные не были предоставлены.',
                                               code='not_authenticated')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_post_not_author(self):
        response = self.not_author.delete('/api/v1/1/')
        expected_data = {'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                               code='permission_denied')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_post_author(self):
        response = self.auth_client.delete('/api/v1/1/')
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(pk=1)
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_post_fields_required(self):
        response = self.auth_client.post('/api/v1/')
        expected_data = {'author': [ErrorDetail(string='Обязательное поле.', code='required')],
                         'title': [ErrorDetail(string='Обязательное поле.', code='required')],
                         'body': [ErrorDetail(string='Обязательное поле.', code='required')]}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserViewSetTestCase(Settings):  # python manage.py test blog.tests.test_views.UserViewSetTestCase

    def test_api_get_many_users_unauth(self):
        response = self.client.get('/api/v1/users/')
        serializer = UserSerializer([self.test_user, self.test_user2, self.admin], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_many_users_auth(self):
        response = self.auth_client.get('/api/v1/users/')
        serializer = UserSerializer([self.test_user, self.test_user2, self.admin], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_many_users_invalid_request(self):
        response = self.client.get('/api/v1/useeeers/')
        expected_data = {'detail': ErrorDetail(string='Страница не найдена.', code='not_found')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_get_one_user_unauth(self):
        response = self.client.get('/api/v1/users/1/')
        serializer = UserSerializer(self.test_user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_one_user_auth(self):
        response = self.auth_client.get('/api/v1/users/1/')
        serializer = UserSerializer(self.test_user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_one_user_invalid_request(self):
        response = self.client.get('/api/v1/users/100/')
        expected_data = {'detail': ErrorDetail(string='Страница не найдена.', code='not_found')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_add_user_unauth(self):
        response = self.client.post('/api/v1/users/', data={'username': 'Added_user'},
                                    content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='Учетные данные не были предоставлены.',
                                               code='not_authenticated')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_add_user_auth(self):
        response = self.auth_client.post('/api/v1/users/', data={'username': 'Added_user'},
                                         content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                               code='permission_denied')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_add_user_admin_auth(self):
        response = self.admin_client.post('/api/v1/users/', data={'username': 'Added_user'},
                                          content_type='application/json')
        added_user = get_user_model().objects.get(pk=response.data['id'])
        serializer = UserSerializer(added_user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_patch_user_unauth(self):
        response = self.client.patch('/api/v1/users/1/', data={'username': 'Patched_user'},
                                     content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='Учетные данные не были предоставлены.',
                                               code='not_authenticated')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_user_auth(self):
        response = self.auth_client.patch('/api/v1/users/1/', data={'username': 'Patched_user'},
                                          content_type='application/json')
        expected_data = {'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                               code='permission_denied')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_user_admin_auth(self):
        response = self.admin_client.patch('/api/v1/users/1/', data={'username': 'Patched_user'},
                                           content_type='application/json')
        added_user = get_user_model().objects.get(pk=response.data['id'])
        serializer = UserSerializer(added_user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_delete_user_unauth(self):
        response = self.client.delete('/api/v1/users/2/')
        expected_data = {'detail': ErrorDetail(string='Учетные данные не были предоставлены.',
                                               code='not_authenticated')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_user_auth(self):
        response = self.auth_client.delete('/api/v1/users/2/')
        expected_data = {'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                               code='permission_denied')}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_user_admin_auth(self):
        response = self.admin_client.delete('/api/v1/users/2/')
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(pk=2)
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_user_fields_required(self):
        response = self.admin_client.post('/api/v1/users/')
        expected_data = {'username': [ErrorDetail(string='Обязательное поле.', code='required')]}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
