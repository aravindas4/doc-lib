import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_short_uuid():
    """Generate Short UUID."""
    return str(uuid.uuid4()).replace("-", "")[:10].upper()


class BaseModel(models.Model):
    """
    Abstract model that acts as parent all the concrete models in the project.
    """

    # Makes sure that an pk is tamper-proof and unpredictable
    id = models.CharField(
        max_length=12, default=get_short_uuid, editable=False, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """
    Custom User class.

    This is added so that in the future more fields related to user can added.
    """

    def __str__(self):
        return f"{self.get_username()}, {self.email} ({self.id})"


class Document(BaseModel):
    """The model that represents the uploaded document."""

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="documents"
    )
    # Local file storage reference
    file = models.FileField(blank=True, upload_to="documents")

    # Shared users
    shared_users = models.ManyToManyField(
        User,
        through="UserDocument",  # Explicit because to add future changes
        related_name="shared_documents",
    )

    class Meta:
        verbose_name_plural = "Documents"
        ordering = ("-created_at",)  # Latest first

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if self.pk is None:  # Creation time
            pass

        super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )


class UserDocument(BaseModel):
    """
    Intermediate model that stores relationship between users and shared
    documents.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_documents"
    )
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="user_documents"
    )

    class Meta:
        verbose_name_plural = "User Documents"
