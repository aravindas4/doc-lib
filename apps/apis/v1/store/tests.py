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
        # Create
        # Act
        response = self.client.post(self.list_url, data={})

        # Assert
        self.assertEqual(response.status_code, 401)

        # List
        # Act
        response = self.client.get(self.list_url)

        # Assert
        self.assertEqual(response.status_code, 401)

        # Detail
        # Act
        response = self.client.get(self.default_url)

        # Assert
        self.assertEqual(response.status_code, 401)

        # Put
        # Act
        response = self.client.put(self.default_url, data={})

        # Assert
        self.assertEqual(response.status_code, 401)

        # Patch
        # Act
        response = self.client.patch(self.default_url, data={})

        # Assert
        self.assertEqual(response.status_code, 401)

        # Delete
        # Act
        response = self.client.delete(self.default_url)

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        # Arrange
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.default.owner)
        )
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.default.id,
                    "owner": self.default.owner_id,
                    "file_url": None,
                }
            ],
        }

        # Act
        response = self.client.get(self.list_url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_detail(self):
        # Arrange
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.default.owner)
        )
        expected_response = {
            "id": self.default.id,
            "owner": self.default.owner_id,
            "file_url": None,
        }

        # Act
        response = self.client.get(self.default_url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_post(self):
        # Arrange
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.default.owner)
        )
        data = {}
        base_response = {"owner": self.default.owner_id, "file_url": None}

        # Act
        response = self.client.post(self.list_url, data=data)
        document_id = response.json().get("id")  # It is unpredictable
        expected_response = {
            **base_response,
            "id": document_id,
            "file_url": f"/documents/{document_id}.txt",
        }

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_response)

    def test_put(self):
        pass

    def test_patch(self):
        pass

    def test_delete(self):
        pass
