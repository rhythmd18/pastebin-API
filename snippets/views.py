from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer


@csrf_exempt  # disable CSRF protection for this view, which is necessary when using the API from a client that doesn't include CSRF tokens
def snippet_list(request: HttpRequest) -> HttpResponse:
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        # serialize the queryset of snippets and set many=True to indicate that we are serializing a list of objects
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        # parse the incoming JSON data from the request body and convert it into a Python dictionary
        data = JSONParser().parse(request)
        # create a new instance of the SnippetSerializer with the parsed data and validate it
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        # try to retrieve the snippet with the given primary key (pk) from the database
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # if the snippet does not exist, return a 404 Not Found response
        return HttpResponse(status=404)

    # Retrieve the snippet
    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    # Update the snippet
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        # create a new instance of the SnippetSerializer with the existing snippet instance and the parsed data, and validate it
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    # Delete the snippet
    elif request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)
