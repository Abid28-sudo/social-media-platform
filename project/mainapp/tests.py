from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Comment, Post


class MainAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.client = Client()
        self.client.login(username='tester', password='testpass')

    def test_create_post_view(self):
        response = self.client.post(
            reverse('create_post'),
            data={'text': 'Hello world'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(text='Hello world', user=self.user).exists())

    def test_toggle_like(self):
        post = Post.objects.create(user=self.user, text='Like test')
        response = self.client.get(reverse('toggle_like', args=[post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(post.likes.filter(user=self.user).exists())

    def test_post_detail_comment(self):
        post = Post.objects.create(user=self.user, text='Comment test')
        response = self.client.post(
            reverse('post_detail', args=[post.id]),
            data={'text': 'Nice post!'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=post, user=self.user, text='Nice post!').exists())

    def test_profile_view(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_login_page_renders(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_signup_page_renders(self):
        self.client.logout()
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up')

    def test_signup_creates_user_and_redirects(self):
        self.client.logout()
        response = self.client.post(
            reverse('signup'),
            data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'complexpass123',
                'password2': 'complexpass123',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_home_redirects_anonymous_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_logout_clears_session(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
        self.assertNotIn('_auth_user_id', self.client.session)
