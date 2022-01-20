from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from apps.store.factory import DocumentFactory


class APITest(TestCase):
    """Base APITest class."""

    @classmethod
    def setUpTestData(cls):
        """Setup base for tests."""
        super().setUpTestData()
        cls.client = APIClient()

    @staticmethod
    def get_auth_header(user):
        """Get Auth token."""
        token_key = user.get_token()
        return f"Token {token_key}"


class DocumentAPITest(APITest):
    @classmethod
    def setUpTestData(cls):
        """Setup base data for tests."""
        super().setUpTestData()
        cls.default = DocumentFactory()  # Default instance
        # Urls
        cls.list_url = reverse("store:document-list")  # common list
        detail_url_name = "store:document-detail"
        cls.default_url = reverse(
            detail_url_name, kwargs={"pk": cls.default.id}
        )

    def test_no_auth(self):
        pass

    def test_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.default.owner)
        )
        response = self.client.get(self.recruiter_details_url)
        self.assertEqual(response.status_code, 405)

    def test_detail(self):
        pass

    def test_put(self):
        pass

    def test_patch(self):
        pass

    def test_delete(self):
        pass
