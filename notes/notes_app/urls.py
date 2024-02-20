from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.urlpatterns import format_suffix_patterns

from notes.notes_app import views
from notes.notes_app.views import SignupView

urlpatterns = [
    path('login', ObtainAuthToken.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('notes/create', views.NotesCreateView.as_view(), name='notes_create'),
    path('notes/share/<str:pk>', views.NoteCollaboratorView.as_view(), name='notes_share'),
    path('notes/version-history/<str:pk>', views.NoteVersionHistoryView.as_view(), name='notes_version_history'),
    path('notes/<str:pk>', views.NotesDetailView.as_view(), name='notes_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
