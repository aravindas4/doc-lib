from django.test import TestCase

from rest_framework.test import APIClient


class APITest(TestCase):
    """Base APITest class."""

    def setUp(self):
        """Setup base for tests."""
        super().setUp()
        self.client = APIClient()

    @staticmethod
    def get_auth_header(user):
        """Get Auth token."""
        token_key = user.get_token()
        return f"Token {token_key}"
