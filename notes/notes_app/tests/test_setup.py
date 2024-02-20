from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from notes.notes_app.models import Note


class TestSetup(APITestCase):
    def setUp(self):
        self.user_data = {'username': 'testuser', 'email': 'testuser@mail.com', 'password': 'testpassword'}
        self.user = User.objects.create_user(**self.user_data)

        self.shared_user_data = {'username': 'shareduser', 'email': 'shareduser@mail.com', 'password': 'sharedpassword'}
        self.shared_user = User.objects.create_user(**self.shared_user_data)

        self.token = Token.objects.get_or_create(user_id=self.user.pk)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.note_data = {'title': 'Test Note', 'content': 'This is a test note.', 'owner': self.user}
        self.note = Note.objects.create(**self.note_data)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
