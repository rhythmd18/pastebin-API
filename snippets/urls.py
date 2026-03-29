from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# add format suffixes to the URL patterns, allowing clients to specify the desired format of the response
# (e.g., JSON, XML) by appending a suffix to the URL (e.g., /snippets.json or /snippets.xml)
urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root, name="root"),
        path("snippets/", views.SnippetList.as_view(), name="snippet-list"),
        path(
            "snippets/<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"
        ),
        path(
            "snippets/<int:pk>/highlight/",
            views.SnippetHighlight.as_view(),
            name="snippet-highlight",
        ),
        path("users/", views.UserList.as_view(), name="user-list"),
        path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
        path("api-auth/", include("rest_framework.urls")),
    ]
)
