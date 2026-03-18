from rest_framework import serializers

from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.ModelSerializer):
    """Serializer for the Snippet model"""

    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style"]
