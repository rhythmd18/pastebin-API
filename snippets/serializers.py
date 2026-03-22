from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    """Serializer for the Snippet model"""

    # the owner field will be a read-only field 
    # that displays the username of the owner of the snippet
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style", "owner"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    # the snippets field will be a primary key related field
    # that allows us to see the snippets created by the user
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "snippets"]
