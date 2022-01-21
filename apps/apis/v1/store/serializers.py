from rest_framework import serializers

from apps.store.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.ReadOnlyField()

    class Meta:
        model = Document
        fields = ("id", "owner", "file_url")
        extra_kwargs = {
            # As the field is captured while saving the serializer
            "owner": {"required": False}
        }

    def create(self, validated_data):
        """
        If the serializer is used, then associated methods are called
        once the instance is created.
        """
        instance = super().create(validated_data)

        # Create file object
        instance.create_document()

        # Since file object is created
        instance.refresh_from_db()
        return instance


class StringListSerializer(serializers.Serializer):
    id_list = serializers.ListField(
        child=serializers.CharField(min_length=1), required=True
    )
