from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import User

from .models import Snippet
from .serializers import APIRootSerializer, SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


@extend_schema(responses=APIRootSerializer)
@api_view(["GET"])
def api_root(request: Request, format=None) -> Response:
    """
    The API's entry point, providing links to the user and snippet list views.
    """
    if request.user.is_authenticated:
        return Response(
            {
                "snippets": reverse("snippet-list", request=request, format=format),
                "users": reverse("user-list", request=request, format=format),
                "logout": request.build_absolute_uri("/api/auth/logout/"),
            }
        )
    return Response(
        {
            "login": request.build_absolute_uri("/api/auth/login/"),
            "register": request.build_absolute_uri("/api/auth/registration/"),
        }
    )


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.

    Addtionally, we also provide an extra `highlight` action.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request: Request, *args, **kwargs) -> Response:
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer: SnippetSerializer) -> None:
        """Set the owner of the snippet to the user making the request."""
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
