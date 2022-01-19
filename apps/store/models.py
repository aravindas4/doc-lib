from django.db import models

from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """
    Abstract model that acts as parent all the concreate models in the project.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=250, null=True, blank=True)
    modified_by = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True


# class User(AbstractUser, BaseModel):
#
#     def __str__(self):
#         return f"{self.get_username()}, {self.email} ({self.id})"
#
#     def save(self, *args, **kwargs):
#
#         # Make sure all the letters in email are lower
#         if self.email and self.email.islower() is False:
#             self.email = self.email.lower()
#
#         if self.username.islower() is False:
#             self.username = self.username.lower()
#
#         return super().save(*args, **kwargs)
