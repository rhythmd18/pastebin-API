from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(r"snippets", views.SnippetViewSet, basename="snippet")
router.register(r"users", views.UserViewSet, basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", views.api_root, name="root"),
    path("", include(router.urls)),
]
