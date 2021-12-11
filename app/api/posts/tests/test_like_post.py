import json
from .base_test import TestBaseCase
from ...helpers.constants import SUCCESS_MESSAGE


class TestLikePost(TestBaseCase):
    """Test class for liking posts."""

    def test_like_post_succeeds(self):
        """Test like a post."""
        response = self.like_post()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['likes'], 1)

    def test_like_own_post_fails(self):
        """Test like own post"""
        response = self.like_your_post()
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', str(response.data))
