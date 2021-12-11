

from os import read
from rest_framework import serializers
from .models import Like, Post
from ..authentication.serializers import RegistrationSerializer


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new post
    """
    title = serializers.CharField(max_length=100, required=True)
    body = serializers.CharField(max_length=1000, required=True)
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ['id','title', 'body', 'author', 'created_at']



class PostRetrieveUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new post
    """
    title = serializers.CharField()
    body = serializers.CharField()
    author = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField()


    @staticmethod
    def get_likes(obj):
        likes = Like.objects.filter(post=obj)
        return likes.count()

    def get_author(self, obj):
        author_info = RegistrationSerializer(obj.author).data
        del author_info['token']
        return author_info

    class Meta:
        model = Post
        fields = ['id','title', 'body', 'author', 'created_at', 'likes']


class PostLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new post
    """
    user = serializers.CharField()
    post = serializers.CharField()


    @staticmethod
    def validate_like(user, post):
        if user.id == post.author.id:
            raise serializers.ValidationError("You cannot like your own post")

    def create(self, validated_data):
        like = Like.objects.filter(user=validated_data['user'], post=validated_data['post']).first()
        if like:
            like.delete()
            return
        return Like.objects.create(**validated_data)



    class Meta:
        model = Like
        fields = ['user','post']