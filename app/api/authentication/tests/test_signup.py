import json
from unittest.mock import patch, Mock
from rest_framework import status
from requests.models import Response
from .base_test import TestBaseCase, User
from ...helpers.constants import SIGNUP_SUCCESS_MESSAGE
from ...helpers.geolocation_data import trigger_geolocation_info_enrichment


# mock response
mock_response = Response()
mock_response.status_code = 200
mock_response._content = b'{"country_code": "KE"}'

class RegistrationTest(TestBaseCase):
    """
    User signup test cases
    """
    @patch('app.api.authentication.views.send_mail_', Mock(return_value=True))
    @patch('requests.get', Mock(return_value=mock_response))
    @patch('app.api.authentication.views.trigger_geolocation_info_enrichment', Mock(return_value=True))
    def test_user_signup_succeed(self):
        """Test API can successfully register a new user"""
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], SIGNUP_SUCCESS_MESSAGE)

    def test_user_signup_with_blank_fields_fails(self):
        """Test register a new user with missing details"""
        response = self.signup_user_with_missing_fields()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors':
            {'email': ['Enter a valid email address.']}, 'status': 'failed'})

    def test_user_signup_with_invalid_email_fails(self):
        """Test register a new user with empty fields"""
        response = self.signup_user_two_with_invalid_email()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors':
            {'email': ['Enter a valid email address.']}, 'status': 'failed'})

    @patch('app.api.authentication.views.send_mail_', Mock(return_value=True))
    @patch('requests.get', Mock(return_value=True))
    @patch('app.api.authentication.views.trigger_geolocation_info_enrichment', Mock(return_value=True))
    def test_signup_existing_user(self):
        """Test register existing user"""
        response = self.signup_existing_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['errors']['email'], ['Email already exist.'])