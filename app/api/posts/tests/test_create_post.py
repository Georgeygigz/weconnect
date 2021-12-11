import json
from .base_test import TestBaseCase
from ...helpers.constants import SUCCESS_MESSAGE


class TestCreatePost(TestBaseCase):
    """Test class for creating a post."""

    def test_create_post_succeeds(self):
        """Test for creating a post."""
        response = self.create_a_post()
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', str(response.data))
        self.assertIn(SUCCESS_MESSAGE.format('post created'), str(response.data['message']))


    def test_create_post_with_missing_fields_fails(self):
        """Test for creating a post with missing fields."""
        response = self.create_a_post_with_missing_fields()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', str(response.data))
        self.assertEqual(json.loads(response.content)['errors'],
            {'title': ['This field is required.']})


    def test_create_post_without_token_fails(self):
        """Test for creating a post with invalid user."""
        response = self.create_a_post_with_invalid_user()
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            b'Authentication credentials were not provided', response.content)