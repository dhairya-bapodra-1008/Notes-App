from rest_framework import permissions


class IsNoteOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNoteOwnerOrCollaborator(permissions.BasePermission):
    """
    Custom permission to only allow owners or collaborators of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or obj.collaborators.filter(pk=request.user.pk).exists()
