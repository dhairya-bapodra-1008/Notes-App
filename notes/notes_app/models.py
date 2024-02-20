import uuid

from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(max_length=100)
    content = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    collaborators = models.ManyToManyField(User, related_name='shared_notes')


class NoteVersionHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='versions')
    changes = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_note_versions')

    class Meta:
        ordering = ['created_at']
