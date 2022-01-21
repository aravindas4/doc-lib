from typing import AnyStr

from rest_framework import serializers

from apps.store.models import Document, User


class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.ReadOnlyField()

    class Meta:
        model = Document
        fields = ("id", "owner", "file_url")
        extra_kwargs = {
            # Because the field is captured while saving the serializer
            "owner": {"required": False}
        }

    def create(self, validated_data):
        """
        :param validated_data:
        :return: instance

        In order to call the associated methods after the has been instance
        created.
        """
        instance = super().create(validated_data)

        # Create file object
        instance.create_document()

        # Since file object is created
        instance.refresh_from_db()
        return instance

    def update(self, instance, validated_data):
        """
        :param instance:
        :param validated_data:
        :return: instance

        In order to call the methods after an instance has been updated.
        """
        instance = super().update(instance, validated_data)
        api_caller: User = self.context.get("api_caller")
        user_type: AnyStr = instance.get_user_type(api_caller)
        operation: AnyStr = "Edit"

        if self.partial is False:  # This is a re-upload
            operation = "Upload"

            # Truncate the file content
            instance.truncate_the_file_content()

        # Log the edit operation
        instance.append_content_to_file(f"{user_type} - {operation}")
        return instance


class StringListSerializer(serializers.Serializer):
    """Expects a list of strings."""

    id_list = serializers.ListField(
        child=serializers.CharField(min_length=1), required=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name")
