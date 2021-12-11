import jwt

from django.utils.timezone import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from app.api.models import BaseModel


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.
    """

    def create_user(self, *args, **kwargs):
        """Create and return a `User` with an email, username and password."""
        password = kwargs.get("password", "")
        email = kwargs.get("email", "")

        del kwargs["password"]
        del kwargs["email"]

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, *args, **kwargs):
        """
        Create and return a User with superuser permissions.
        """
        password = kwargs.get("password", "")
        email = kwargs.get("email", "")

        del kwargs["password"]
        del kwargs["email"]

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model"""

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    location_info = models.JSONField(default=dict)
    holiday_info = models.JSONField(default=dict)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        """Returns string representation of user"""
        return self.email

    @property
    def token(self):
        """Method that generates and returns a string of the
        token generated.
        """
        date = datetime.now() + timedelta(hours=settings.TOKEN_EXP_TIME)
        payload = {
            "email": self.email,
            "exp": int(date.strftime("%s")),
            "id": self.id,
            "username": self.username,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token
