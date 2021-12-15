import json
from .base_test import TestBaseCase
from ...helpers.constants import SUCCESS_MESSAGE


class TestRetrievePost(TestBaseCase):
    """Test class for retrieving posts."""

    def test_retrieve_posts_succeeds(self):
        """Test for retrieving a post."""
        response = self.retrieve_posts()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', str(response.data))
        self.assertIn(SUCCESS_MESSAGE.format('posts retrieved'), str(response.data['message']))
        self.assertEqual(len(response.data['data']), 0)

    def test_retrieve_created_posts_succeeds(self):
        """Test retrieve created posts."""
        response, data = self.retrieve_created_posts()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', str(response.data))
        self.assertIn(SUCCESS_MESSAGE.format('posts retrieved'), str(response.data['message']))
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], data['title'])

    def test_retrieve_single_posts_succeeds(self):
        """Test retrieve single posts."""
        response = self.retrieve_single_post()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', str(response.data))
        self.assertIn(SUCCESS_MESSAGE.format('post retrieved'), str(response.data['message']))
        self.assertEqual(type(response.data), dict)

    def test_retrieve_non_existing_post_fails(self):
        """Test retrieve non existing post."""
        response = self.retrieve_non_existing_post()
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', str(response.data))

    def test_retrieve_my_post_succeeds(self):
        """Test my posts post."""
        response = self.retrieve_my_posts()
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', str(response.data))
        self.assertIn(SUCCESS_MESSAGE.format('posts retrieved'), str(response.data['message']))

    def test_retrieve_my_post_without_token_fails(self):
        """Test for creating a post with invalid user."""
        response = self.retrieve_my_posts_without_token()
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            b'Authentication credentials were not provided', response.content)

