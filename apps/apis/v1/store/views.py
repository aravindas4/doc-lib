from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.store.models import Document

from .serializers import DocumentSerializer, StringListSerializer


class DocumentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer
    model = Document
    queryset = model.objects.all()

    def get_queryset(self):
        # Owner
        return self.queryset.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        # Saving the owner of the document
        serializer.save(owner=self.request.user)

    @action(methods=["POST"], detail=True, url_path="share")
    def share(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StringListSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        instance.add_shared_users(serializer.validated_data["id_list"])
        return self.retrieve(request, *args, **kwargs)
