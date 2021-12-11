import json
from .base_test import TestBaseCase
from rest_framework.views import status
from app.api.helpers.tasks import send_mail_
from ...helpers.serialization_errors import error_dict


class UserLoginTest(TestBaseCase):

    def test_user_login_succeeds(self):
        """if user is registered"""
        response = self.login_user_successfull()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('email', response.data['data'])
        self.assertIn('token', response.data['data'])

    def test_login_unregistered_user_fails(self):
        """Test login for unregistered users"""
        response = self.login_user_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)