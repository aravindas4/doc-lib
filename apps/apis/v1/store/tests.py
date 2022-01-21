from django.urls import reverse

from apps.store.factory import (
    DocumentFactory,
    UserFactory,
    UserDocumentFactory,
)
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

        # Share
        # Act
        response = self.client.post(f"{self.default_url}share/", data={})

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_list(self):
        # Case 1: Owner
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

        # Case 2: Non shared User
        # Arrange
        user1 = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user1))
        expected_response = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
        }

        # Act
        response = self.client.get(self.list_url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

        # Case: Shared User
        # Arrange
        UserDocumentFactory(user=user1, document=self.default)
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
        # Case 1: Owner
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

        # Case 2: Non shared User
        # Arrange
        user1 = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user1))
        expected_response = {"detail": "Not found."}

        # Act
        response = self.client.get(self.default_url)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_response)

        # Case: Shared User
        # Arrange
        UserDocumentFactory(user=user1, document=self.default)
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

    def test_share(self):
        # Case 1: First attempt
        # Arrange
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.default.owner)
        )
        url_name = "store-v1:document-share"
        url = reverse(url_name, kwargs={"pk": self.default.id})
        user1 = UserFactory()
        data = {"id_list": [user1.id, "HHHHHHHHH"]}  # Invalid ID
        expected_response = {
            "id": self.default.id,
            "owner": self.default.owner_id,
            "file_url": None,
        }

        # Act
        response = self.client.post(url, data=data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)
        # Maks sure that user is added to the shared list
        self.assertTrue(self.default.shared_users.filter(id=user1.id).exists())
        # Only 1 user is present
        self.assertEqual(self.default.shared_users.count(), 1)

        # Case 2: Try again
        # Arrange
        user2 = UserFactory()
        data = {
            "id_list": [
                user1.id,  # Already added
                user2.id,  # New
                "HHHHHHHHH",  # Invalid ID
            ]
        }
        expected_response = {
            "id": self.default.id,
            "owner": self.default.owner_id,
            "file_url": None,
        }

        # Act
        response = self.client.post(url, data=data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)
        # Maks sure that user is added to the shared list
        self.assertTrue(self.default.shared_users.filter(id=user2.id).exists())
        # Only 2 users are present
        self.assertEqual(self.default.shared_users.count(), 2)

        # Case 2: Non owner tries to share
        # Arrange
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user1))
        data = {
            "id_list": [
                user1.id,  # Already added
                user2.id,  # New
                "HHHHHHHHH",  # Invalid ID
            ]
        }
        expected_response = {"detail": "Not found."}

        # Act
        response = self.client.post(url, data=data)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_response)

    def test_put(self):
        pass

    def test_patch(self):
        pass

    def test_delete(self):
        # Case 1: Non shared User
        # Arrange
        user1 = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=self.get_auth_header(user1))
        expected_response = {"detail": "Not found."}

        # Act
        response = self.client.delete(self.default_url)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_response)

        # Case 2: Shared User
        # Arrange
        UserDocumentFactory(user=user1, document=self.default)

        # Act
        response = self.client.delete(self.default_url)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_response)

        # Case 3: Owner
        # Arrange
        self.client.credentials(
            HTTP_AUTHORIZATION=self.get_auth_header(self.default.owner)
        )

        # Act
        response = self.client.delete(self.default_url)

        # Assert
        self.assertEqual(response.status_code, 204)
