from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from ..models import User

class TestBaseCase(APITestCase):
    def setUp(self):
        self.login_url = api_reverse('authentication:user-login')
        self.signup_url = api_reverse('authentication:user-registration')
        self.create_post_url = api_reverse('posts:post-create')
        self.retrieve_my_posts_url = api_reverse('posts:posts-retrieve-all')

        self.valid_user = {
            'username': 'mary',
            'email': 'mary@mary.com',
            'password': 'Pass@123',
        }

        self.valid_post = {
            'title': 'test title',
            'body': 'test body',
        }

        self.user_one = User.objects.create_user(
            username='mary',
            email='mary@mary.com',
            password='Pass@123',
            is_active=True
        )

        self.user_two = User.objects.create_user(
            username='mary1',
            email='mary1@mary.com',
            password='Pass@123',
            is_active=True
        )


    def create_a_post(self):
        """create a post"""
        response = self.client.post(
            self.create_post_url, self.valid_post, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.user_one.token))
        return response

    def create_a_post_with_missing_fields(self):
        """create a post with missing fields"""

        del self.valid_post['title']
        response = self.client.post(
            self.create_post_url, self.valid_post, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.user_one.token))
        return response

    def create_a_post_with_invalid_user(self):
        """create a post with invalid user"""
        response = self.client.post(
            self.create_post_url, self.valid_post, format='json')
        return response

    def retrieve_posts(self):
        """Retrieve posts"""
        response = self.client.get(
            self.create_post_url, self.valid_post, format='json')
        return response

    def retrieve_created_posts(self):
        """Retrieve created posts"""
        self.create_a_post()
        response = self.client.get(
            self.create_post_url, self.valid_post, format='json')
        return response, self.valid_post

    def retrieve_single_post(self):
        """Retrieve single post"""
        post = self.create_a_post()
        response = self.client.get(
           api_reverse('posts:posts-retrieve-update-delete', args=[post.data['data']['id']]))
        return response

    def retrieve_non_existing_post(self):
        """Retrieve non existing post"""
        response = self.client.get(
           api_reverse('posts:posts-retrieve-update-delete', args=[123]))
        return response

    def retrieve_my_posts(self):
        """Retrieve my posts"""
        response = self.client.get(
            self.retrieve_my_posts_url, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.user_one.token))
        return response

    def retrieve_my_posts_without_token(self):
        """retrieve_my_posts_without_token"""
        response = self.client.get(
            self.retrieve_my_posts_url, format='json')
        return response


    def update_post(self):
        """Update post"""
        post = self.create_a_post()
        response = self.client.patch(
           api_reverse('posts:posts-retrieve-update-delete', args=[post.data['data']['id']]),
           self.valid_post,
           HTTP_AUTHORIZATION ='token {}'.format(self.user_one.token))
        return response

    def update_non_existing_post(self):
        """Update non existing post"""
        response = self.client.patch(
           api_reverse('posts:posts-retrieve-update-delete', args=[123]),
           self.valid_post,
           HTTP_AUTHORIZATION ='token {}'.format(self.user_one.token))
        return response

    def delete_post(self):
        """Update non existing post"""
        post = self.create_a_post()
        response = self.client.delete(
           api_reverse('posts:posts-retrieve-update-delete', args=[post.data['data']['id']]),
           HTTP_AUTHORIZATION ='token {}'.format(self.user_one.token))
        return response

    def like_post(self):
        """Like post"""
        post = self.create_a_post()
        self.client.get(
           api_reverse('posts:post-like', args=[post.data['data']['id']]),
           HTTP_AUTHORIZATION ='token {}'.format(self.user_two.token))

        single_post = self.client.get(
           api_reverse('posts:posts-retrieve-update-delete', args=[post.data['data']['id']]))
        return single_post

    def like_your_post(self):
        """Like your post"""
        post = self.create_a_post()
        response = self.client.get(
           api_reverse('posts:post-like', args=[post.data['data']['id']]),
           HTTP_AUTHORIZATION ='token {}'.format(self.user_one.token))

        return response

