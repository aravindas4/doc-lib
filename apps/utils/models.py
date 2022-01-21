import uuid

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
