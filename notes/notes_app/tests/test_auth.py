from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from notes.notes_app.tests.test_setup import TestSetup


class TestAuthViews(TestSetup):

    def test_signup(self):
        url = reverse('signup')
        data = {'username': 'testuser2', 'email': 'testuser2@mail.com', 'password': 'testuser2@123'}
        old_count = User.objects.count()

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), old_count + 1)

    def test_signup_duplicate_username(self):
        url = reverse('signup')
        data = {'username': self.user.username, 'email': 'testuser2@mail.com', 'password': 'testpassword2'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_duplicate_email(self):
        url = reverse('signup')
        data = {'username': 'testuser2', 'email': self.user.email, 'password': 'testpassword2@123'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        url = reverse('login')
        data = {'username': self.user_data['username'], 'password': self.user_data['password']}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('token', ''), self.token.key)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {'username': 'test', 'password': 'test'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'username': self.user_data['username'], 'password': 'test'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
