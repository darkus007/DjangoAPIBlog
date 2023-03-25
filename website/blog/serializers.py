from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()    # в случае своей модели пользователя, вернет ее
        fields = ('id', 'username',)
