import json
from .base_test import TestBaseCase
from ...helpers.constants import SUCCESS_MESSAGE


class TestRetrievePost(TestBaseCase):
    """Test class for retrieving posts."""

    def test_update_posts_succeeds(self):
        """Test for retrieving a post."""
        response = self.update_post()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', str(response.data))
        self.assertIn(SUCCESS_MESSAGE.format('post updated'), str(response.data['message']))

    def test_update_non_existing_post_fails(self):
        """Test retrieve non existing post."""
        response = self.update_non_existing_post()
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', str(response.data))

    def test_delete_post_succeeds(self):
        """Test retrieve non existing post."""
        response = self.delete_post()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', str(response.data))


