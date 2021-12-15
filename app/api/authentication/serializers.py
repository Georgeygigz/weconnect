from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from ..helpers.serialization_errors import error_dict


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure email is provided and is unique
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict["already_exist"].format("Email"),
            )
        ],
        error_messages={
            "required": error_dict["required"],
        },
    )
    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        min_length=8,
        max_length=30,
        required=True,
        allow_null=False,
        write_only=True,
        error_messages={
            "required": error_dict["required"],
            "min_length": error_dict["min_length"].format("Password", "8"),
            "max_length": "Password cannot be more than 30 characters",
            "invalid": error_dict["invalid_password"],
        },
    )

    username = serializers.RegexField(
        regex="^(?!.*\ )[A-Za-z\d\-\_]+$",
        allow_null=False,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=error_dict["already_exist"].format("Username"),
            )
        ],
        error_messages={
            "required": error_dict["required"],
            "invalid": error_dict["invalid_name"].format("Username"),
        },
    )

    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token", 'id']

    def create(self, data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**data)



class LoginSerializer(serializers.Serializer):
    """Login serializer Class"""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    @staticmethod
    def validate(data):
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(email=email, password=password)


        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        return {
            'email': user.email,
            'token': user.token
        }