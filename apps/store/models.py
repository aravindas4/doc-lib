import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_short_uuid():
    """Generate Short UUID."""
    return str(uuid.uuid4()).replace("-", "")[:10].upper()


class BaseModel(models.Model):
    """
    Abstract model that acts as parent all the concreate models in the project.
    """

    # Makes sure that an pk is tamper-proof and unpredictable
    id = models.CharField(
        max_length=12, default=get_short_uuid, editable=False, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=250, null=True, blank=True)
    modified_by = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """
    Custom User class.

    This is added so that in the future more fields related to user can added.
    """

    def __str__(self):
        return f"{self.get_username()}, {self.email} ({self.id})"
