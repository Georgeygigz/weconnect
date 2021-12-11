from django.urls import path
from .views import RegistrationAPIView, VerifyAPIView,LoginApiView


urlpatterns = [
    path("signup", RegistrationAPIView.as_view(), name="user-registration"),
    path("login", LoginApiView.as_view(), name="user-login"),
    path("verify/<str:token>", VerifyAPIView.as_view(), name="user-verification"),
]
