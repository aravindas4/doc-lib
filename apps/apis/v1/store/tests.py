from django.urls import reverse

from apps.store.factory import DocumentFactory
from apps.utils.tests import APITest


class DocumentAPITest(APITest):
    @classmethod
    def setUpTestData(cls):
        """Setup base data for tests."""
        super().setUpTestData()
        cls.default = DocumentFactory()  # Default instance
        # Urls
        cls.list_url = reverse("store-v1:document-list")  # common list
        detail_url_name = "store-v1:document-detail"
        cls.default_url = reverse(
            detail_url_name, kwargs={"pk": cls.default.id}
        )

    def test_no_auth(self):
        pass

    def test_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.default.owner)
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {"id": self.default.id, "owner": self.default.owner_id}
            ],
        }
        self.assertEqual(response.json(), expected_response)

    def test_detail(self):
        pass

    def test_put(self):
        pass

    def test_patch(self):
        pass

    def test_delete(self):
        pass
