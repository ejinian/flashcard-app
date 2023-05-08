from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'

    def test_user_registration(self):
        user = User.objects.create_user(username=self.username, password=self.password)
        self.assertIsNotNone(user.id)

    def test_user_login(self):
        User.objects.create_user(username=self.username, password=self.password)
        response = self.client.post('/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertEqual(response.wsgi_request.user.username, self.username)

    def test_user_logout(self):
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.username, '')