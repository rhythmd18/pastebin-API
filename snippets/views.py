from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetList(APIView):
    """
    List all code snippets, or create a new snippet.
    """

    def get(self, request: Request, format: None = None) -> Response:
        """
        List the code snippets on GET request
        """
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, format: None = None) -> Response:
        """
        Create a new snippet on POST request
        """
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    View a single code snippet, update it, and delete it
    """

    def get_object(self, pk: int) -> Snippet:
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: int, format: None = None) -> Response:
        """
        Display the snippet details on GET request
        """
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int, format: None = None) -> Response:
        """
        Update a snippet on PUT request
        """
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int, format: None = None) -> Response:
        """
        Delete a snippet on DELETE request
        """
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
