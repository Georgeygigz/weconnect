from django.db import models
from ..models import BaseModel
from ..authentication.models import User


class Post(BaseModel):
    """
    Post model
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        """String representation of the model"""
        return self.title


class Like(BaseModel):
    """
    Like model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        """String representation of the model"""
        return f'{self.user} likes {self.post}'