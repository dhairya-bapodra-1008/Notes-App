import json

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from notes.notes_app.models import Note, NoteVersionHistory


def calculate_diff(old, new):
    old_words = old.split()
    new_words = new.split()

    changes = []

    for idx, new_word in enumerate(new_words, start=1):
        if idx > len(old_words) or old_words[idx - 1] != new_word:
            changes.append({'word_no': idx, 'content': new_word})

    return changes


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner']

    def validate_title(self, value):
        if self.instance:
            return value
        user = self.context['request'].user
        existing_notes = Note.objects.filter(owner=user, title=value)
        if existing_notes.exists():
            raise serializers.ValidationError('Note with same title already exists!')
        return value


class NoteUpdateSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner']

    def update(self, instance, validated_data):
        non_editable_fields = ['title', 'owner']

        for non_editable_field in non_editable_fields:
            if non_editable_field in validated_data:
                raise serializers.ValidationError({non_editable_field: [f'This field is not editable.']})

        diff = calculate_diff(instance.content, validated_data['content'])

        instance = super().update(instance, validated_data)
        NoteVersionHistory.objects.create(note=instance, changes=json.dumps(diff),
                                          created_by=validated_data.get('updated_by'))

        return instance


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message='A user with that email already exists!')]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class NoteCollaboratorSerializer(serializers.ModelSerializer):
    collaborators = serializers.ListField(child=serializers.CharField(required=True), required=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ['id', 'collaborators', 'owner']

    def validate_collaborators(self, value):
        for collaborator_username in value:
            if not User.objects.filter(username=collaborator_username).exists():
                raise serializers.ValidationError(f"User with username '{collaborator_username}' not found.")
        return value

    def update_collaborators(self, instance, validated_data):
        collaborators = validated_data['collaborators']

        collaborator_users = [User.objects.get(username=username) for username in collaborators]

        instance.collaborators.add(*collaborator_users)
        return instance


class NoteVersionHistorySerializer(serializers.ModelSerializer):
    changes = serializers.JSONField()
    created_at = serializers.DateTimeField()
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = NoteVersionHistory
        fields = ['changes', 'created_at', 'created_by']
