import uuid

from typing import AnyStr, NoReturn, Union
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings


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

    def __str__(self) -> AnyStr:
        return f"{self.get_username()}, {self.email} ({self.id})"

    def get_token(self) -> AnyStr:
        token, _ = Token.objects.get_or_create(user=self)
        return token.key


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

    def file_url(self) -> Union[AnyStr, None]:
        """Return file url."""
        if self.file:
            return self.file.url
        return None

    def create_document(self) -> NoReturn:
        """Create the document file for the object."""

        if bool(self.file) is False:  # If the file doesn't exist, create
            self.file.save(f"{self.id}.txt", ContentFile(""))
            self.save(update_fields=["file"])
            self.append_content_to_file("Owner - Upload")

    def append_content_to_file(self, content: AnyStr) -> NoReturn:
        """
        If the file exists, append the content to the end along with timestamp.
        """
        if self.file:
            # Format the timestamp details
            timestamp = timezone.localtime(timezone.now()).strftime(
                api_settings.DATETIME_FORMAT
            )
            # Open the file in append mode
            file = open(self.file.path, "a")

            # Add the timestamp details to content
            file.write(f"{timestamp} - {content} \n")
            file.close()


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
