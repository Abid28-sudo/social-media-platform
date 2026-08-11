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
