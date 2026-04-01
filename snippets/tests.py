from django.contrib.auth.models import User
from django.urls import reverse
from typing import cast
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Snippet


class SnippetModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.snippet = Snippet.objects.create(
            title="Test Snippet",
            code="print('Hello, World!')",
            linenos=True,
            language="python",
            style="friendly",
            owner=cls.user,
        )

    def authenticateUser(self):
        cast(APIClient, self.client).force_authenticate(user=self.user)

    def test_snippet_creation(self):
        self.assertEqual(self.snippet.title, "Test Snippet")
        self.assertEqual(self.snippet.code, "print('Hello, World!')")
        self.assertEqual(self.snippet.linenos, True)
        self.assertEqual(self.snippet.language, "python")
        self.assertEqual(self.snippet.style, "friendly")
        self.assertEqual(self.snippet.owner, self.user)

    def test_snippet_listview(self):
        self.authenticateUser()
        response = self.client.get(reverse("snippet-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertContains(response, self.snippet.title)

    def test_snippet_detailview(self):
        self.authenticateUser()
        response = self.client.get(
            reverse("snippet-detail", kwargs={"pk": self.snippet.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertContains(response, self.snippet.title)
