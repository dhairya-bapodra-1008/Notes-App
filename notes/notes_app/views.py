from rest_framework import generics, permissions, status
from rest_framework.authtoken.admin import User
from rest_framework.response import Response

from notes.notes_app.models import Note, NoteVersionHistory
from notes.notes_app.permissions import IsNoteOwner, IsNoteOwnerOrCollaborator
from notes.notes_app.serializers import NoteSerializer, SignupSerializer, NoteCollaboratorSerializer, \
    NoteUpdateSerializer, NoteVersionHistorySerializer


class SignupView(generics.CreateAPIView):
    """
    Create a new user.
    """
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class NotesCreateView(generics.CreateAPIView):
    """
    Create a new note.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NotesDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a note instance.
    """
    queryset = Note.objects.all()
    serializer_class = NoteUpdateSerializer
    permission_classes = [IsNoteOwnerOrCollaborator]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class NoteCollaboratorView(generics.GenericAPIView):
    """
    Add one or more collaborators to a note instance.
    """
    queryset = Note.objects.all()
    serializer_class = NoteCollaboratorSerializer
    permission_classes = [IsNoteOwner]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update_collaborators(instance, serializer.validated_data)
        return Response('Collaborators added successfully!', status=status.HTTP_200_OK)


class NoteVersionHistoryView(generics.ListAPIView):
    """
    Retrieve version history of a note.
    """
    queryset = NoteVersionHistory.objects.all()
    permission_classes = [IsNoteOwnerOrCollaborator]
    serializer_class = NoteVersionHistorySerializer
