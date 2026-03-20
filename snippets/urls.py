from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("snippets/", views.snippet_list, name="snippet_list"),
    path("snippets/<int:pk>/", views.snippet_detail, name="snippet_detail"),
]

# add format suffixes to the URL patterns, allowing clients to specify the desired format of the response
# (e.g., JSON, XML) by appending a suffix to the URL (e.g., /snippets.json or /snippets.xml)
urlpatterns = format_suffix_patterns(urlpatterns)
