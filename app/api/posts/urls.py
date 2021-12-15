from django.urls import path

from .views import (PostCreateListApiView, PostRetrieveUpdateDestroyApiView,PostLikeApiView,
                    PostsRetrieveApiView)

urlpatterns = [
    path('', PostCreateListApiView.as_view(), name='post-create'),
    path('retrieve/myposts', PostsRetrieveApiView.as_view(), name='posts-retrieve-all'),
    path('<str:id>', PostRetrieveUpdateDestroyApiView.as_view(), name='posts-retrieve-update-delete'),
    path('like/<str:id>', PostLikeApiView.as_view(), name='post-like'),
]