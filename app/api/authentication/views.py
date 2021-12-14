from django.shortcuts import render
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics


from ..helpers.renderers import RequestJSONRenderer
from ..helpers.tasks import send_mail_
from ..helpers.token import get_token_data

from .serializers import RegistrationSerializer, LoginSerializer
from ..helpers.constants import SIGNUP_SUCCESS_MESSAGE, SUCCESS_MESSAGE, VERIFICATION_SUCCESS_MSG
from ..helpers.geolocation_data import trigger_geolocation_info_enrichment

# Create your views here.


class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Handle user login
        """
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        data = serializer.data

        user_email = data["email"]
        username = data["username"]

        domain = settings.VERIFY_URL

        url = domain + str(data["token"])

        body = f"Hi {username} click this link to verify your account {url}"
        subject = "Verify your email"
        message = "Please verify your account."
        # send email to the user for verification
        send_mail_.delay(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[user_email],
            html_message=body,
            fail_silently=False,
        )
        # enrich user data
        trigger_geolocation_info_enrichment.delay(data['id'])

        return_message = {"message": SIGNUP_SUCCESS_MESSAGE}
        return Response(return_message, status=status.HTTP_201_CREATED)


class LoginApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handle user login
        """
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        return_message = {"message": SUCCESS_MESSAGE.format('Login'), "data": serializer.data}
        return Response(return_message, status=status.HTTP_200_OK)


class VerifyAPIView(generics.RetrieveAPIView):
    """
    A class to verify user using the token sent to the email
    """

    permission_classes = (AllowAny,)
    renderer_classes = (RequestJSONRenderer,)

    @classmethod
    def get(cls, request, token):
        """
        Overide the default get method
        """
        user = get_token_data(token)
        user.is_active = True
        user.save()
        return Response(
            data={"message": VERIFICATION_SUCCESS_MSG}, status=status.HTTP_200_OK
        )
