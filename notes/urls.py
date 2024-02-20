from django.urls import path, include

urlpatterns = [
    path('api/', include('notes.notes_app.urls')),
]
