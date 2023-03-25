from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=127, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор поста')

    def __str__(self):
        return str(self.title) + " - " + str(self.author)

