from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer


# @csrf_exempt  # disable CSRF protection for this view, which is necessary when using the API from a client that doesn't include CSRF tokens
@api_view(["GET", "POST"])
def snippet_list(request: Request, format: None = None) -> Response:
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        # serialize the queryset of snippets and set many=True to indicate that we are serializing a list of objects
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # create a new instance of the SnippetSerializer data and validate it
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def snippet_detail(request: Request, pk: int, format: None = None) -> Response:
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        # try to retrieve the snippet with the given primary key (pk) from the database
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # if the snippet does not exist, return a 404 Not Found response
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Retrieve the snippet
    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    # Update the snippet
    elif request.method == "PUT":
        # create a new instance of the SnippetSerializer with the existing snippet instance and the parsed data, and validate it
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete the snippet
    elif request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
