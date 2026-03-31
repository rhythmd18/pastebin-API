from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Snippet


class APIRootSerializer(serializers.Serializer):
    """
    Serializer for the API root view, providing links to the user and snippet list views.
    """

    snippets = serializers.URLField(required=False)
    users = serializers.URLField(required=False)
    logout = serializers.URLField(required=False)
    login = serializers.URLField(required=False)
    register = serializers.URLField(required=False)


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Snippet model"""

    # the owner field will be a read-only field
    # that displays the username of the owner of the snippet
    owner = serializers.ReadOnlyField(source="owner.username")

    # the highlight field will be a hyperlinked identity field
    # that allows us to see the highlighted version of the snippet
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight", format="html"
    )

    class Meta:
        model = Snippet
        fields = [
            "url",
            "id",
            "highlight",
            "owner",
            "title",
            "code",
            "linenos",
            "language",
            "style",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the User model.
    """

    # the snippets field will be a hyperlinked related field
    # that allows us to see all the snippets created by the user
    snippets = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="snippet-detail"
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]
