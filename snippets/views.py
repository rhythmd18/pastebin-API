from rest_framework import generics

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new snippet.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View a single code snippet, update it, and delete it
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
