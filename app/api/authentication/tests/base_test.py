from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from ..models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = api_reverse('authentication:user-registration')
        self.login_url = api_reverse('authentication:user-login')

        self.valid_user = {
            'username': 'mary',
            'email': 'mary@mary.com',
            'password': 'Pass@123',
        }

        self.user_with_invalid_email = {
            'username': 'mary',
            'email': 'mary',
            'password': 'Pass@123',
        }

        self.user_with_missing_fields = {
            'username': 'mary',
            'password': 'Pass@123',
        }


    def signup_user_one(self):
        """
        successfully signup user
        """
        self.client.post(
            self.signup_url, self.valid_user, format='json')
        user = User.objects.get(email=self.valid_user['email'])
        user.is_active = True
        user.save()
        return user

    def signup_user_two(self):
        """
        successfully signup user
        """
        self.client.post(
            self.signup_url, self.valid_user, format='json')
        return User.objects.get(email=self.valid_user['email'])

    def signup_user_two_with_invalid_email(self):
        """
        successfully signup user
        """
        response = self.client.post(
            self.signup_url, self.user_with_invalid_email, format='json')
        return response

    def signup_user_with_missing_fields(self):
        """Signup user with missing fields"""
        response = self.client.post(
            self.signup_url, self.user_with_invalid_email, format='json')
        return response

    def signup_existing_user(self):
        """Signup existing user"""
        self.client.post(
            self.signup_url, self.valid_user, format='json')
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')
        return response

    def login_user_successfull(self):
        """Login in user"""
        self.signup_user_one()
        response = self.client.post(
            self.login_url, self.valid_user, format='json')
        return response

    def login_user_fails(self):
        """Login in user with invalid credentials"""
        response = self.client.post(
            self.login_url, self.valid_user, format='json')
        return response