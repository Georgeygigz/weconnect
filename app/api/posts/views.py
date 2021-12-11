from django.db.models import query
from django.shortcuts import render
from django.utils.functional import partition
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .serializers import (PostCreateSerializer, Post, PostRetrieveUpdateSerializer, PostLikeSerializer)
from ..helpers.renderers import RequestJSONRenderer
from ..helpers.constants import SUCCESS_MESSAGE
from .helpers.query_helper import retrieve_post_by_id, validate_author
from ..helpers.permissions import UserPermission

class PostCreateListApiView(generics.ListCreateAPIView):
    permission_classes = (UserPermission,)
    renderer_classes = [RequestJSONRenderer,]
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return_message = {
            "message": SUCCESS_MESSAGE.format('post created'),
            "data": serializer.data

        }
        return Response(return_message, status=201)

    def get(self, request, *args, **kwargs):
        posts = self.queryset.filter(deleted=False)
        serializer = PostRetrieveUpdateSerializer(posts, many=True)
        return_message = {
            "message": SUCCESS_MESSAGE.format('posts retrieved'),
            "data": serializer.data
        }
        return Response(return_message, status=200)


class PostRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [UserPermission,]
    renderer_classes = [RequestJSONRenderer,]
    serializer_class = PostRetrieveUpdateSerializer

    def get(self, request, *args, **kwargs):
        post =  retrieve_post_by_id(Post, kwargs['id'])
        serializer = self.serializer_class(post)
        return_message = {
            "message": SUCCESS_MESSAGE.format('post retrieved'),
            "data": serializer.data
        }
        return Response(return_message, status=200)

    def patch(self, request, *args, **kwargs):
        post =  retrieve_post_by_id(Post, kwargs['id'])
        validate_author(request.user == post.author)
        serializer = self.serializer_class(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return_message = {
            "message": SUCCESS_MESSAGE.format('post updated'),
            "data": serializer.data
        }
        return Response(return_message, status=200)

    def delete(self, request, *args, **kwargs):
        post =  retrieve_post_by_id(Post, kwargs['id'])
        validate_author(request.user == post.author)
        post.delete()
        return_message = {
            "message": SUCCESS_MESSAGE.format('post deleted'),
            "data": {}
        }
        return Response(return_message, status=200)


class PostsRetrieveApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = [RequestJSONRenderer,]
    serializer_class = PostRetrieveUpdateSerializer

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(author=request.user)
        serializer = self.serializer_class(posts, many=True)
        return_message = {
            "message": SUCCESS_MESSAGE.format('posts retrieved'),
            "data": serializer.data
        }
        return Response(return_message, status=200)


class PostLikeApiView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = [RequestJSONRenderer,]
    serializer_class = PostLikeSerializer

    def get(self, request, *args, **kwargs):
        post =  retrieve_post_by_id(Post, kwargs['id'])
        serializer = self.serializer_class(post)
        serializer.validate_like(request.user, post)
        serializer.create({'user':request.user, 'post':post})
        return_message = {
            "message": SUCCESS_MESSAGE.format('liked post'),
        }
        return Response(return_message, status=200)