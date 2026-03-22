from rest_framework import mixins
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    List all code snippets, or create a new snippet.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        List the code snippets
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Create a new snippet
        """
        return self.create(request, *args, **kwargs)


class SnippetDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    View a single code snippet, update it, and delete it
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Get the snippet details
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Update a snippet
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Delete a snippet
        """
        return self.destroy(request, *args, **kwargs)
