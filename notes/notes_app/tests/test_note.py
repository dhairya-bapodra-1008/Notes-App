import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from notes.notes_app.models import Note
from notes.notes_app.tests.test_setup import TestSetup


class TestNoteViews(TestSetup):

    def test_create_note(self):
        url = reverse('notes_create')
        data = {'title': 'New Note', 'content': 'This is a test note.'}
        old_count = Note.objects.count()

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), old_count + 1)

    def test_create_note_without_login(self):
        url = reverse('notes_create')
        data = {'title': 'New Note', 'content': 'This is a test note.'}

        self.client.credentials()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_note_by_id(self):
        url = reverse('notes_detail', kwargs={'pk': self.note.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], self.note.title)
        self.assertEqual(response.json()['content'], self.note.content)

    def test_get_note_without_login(self):
        url = reverse('notes_detail', kwargs={'pk': self.note.id})

        self.client.credentials()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_note_with_invalid_id(self):
        url = reverse('notes_detail', kwargs={'pk': uuid.uuid4()})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_note(self):
        url = reverse('notes_detail', kwargs={'pk': self.note.id})
        data = {'content': 'This is a test note. This line is appended.'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.content, data['content'])

    def test_update_note_without_login(self):
        url = reverse('notes_detail', kwargs={'pk': self.note.id})
        data = {'content': 'This is a test note. This line is appended.'}

        self.client.credentials()
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_note_with_invalid_id(self):
        url = reverse('notes_detail', kwargs={'pk': uuid.uuid4()})
        data = {'content': 'This is a test note. This line is appended.'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_share_note(self):
        url = reverse('notes_share', kwargs={'pk': self.note.id})
        data = {'collaborators': [self.shared_user.username]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.shared_user in self.note.collaborators.all())

    def test_share_note_without_login(self):
        url = reverse('notes_share', kwargs={'pk': self.note.id})
        data = {'collaborators': [self.shared_user.username]}

        self.client.credentials()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_share_note_with_invalid_id(self):
        url = reverse('notes_share', kwargs={'pk': uuid.uuid4()})
        data = {'collaborators': [self.shared_user.username]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_share_note_with_invalid_user(self):
        url = reverse('notes_share', kwargs={'pk': self.note.id})
        data = {'collaborators': ['invalidshareduser']}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_shared_note(self):
        self.note.collaborators.add(self.shared_user)

        token = Token.objects.get_or_create(user_id=self.shared_user.pk)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('notes_detail', kwargs={'pk': self.note.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], self.note.title)
        self.assertEqual(response.json()['content'], self.note.content)

    def test_update_shared_note(self):
        self.note.collaborators.add(self.shared_user)

        token = Token.objects.get_or_create(user_id=self.shared_user.pk)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('notes_detail', kwargs={'pk': self.note.id})
        data = {'content': 'This is a test note. This line is appended.'}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.content, data['content'])

    def test_get_note_version_history(self):
        url = reverse('notes_detail', kwargs={'pk': self.note.id})
        data = {'content': 'This is a test note. This line is appended.'}

        self.client.put(url, data, format='json')

        url = reverse('notes_version_history', kwargs={'pk': self.note.id})

        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
