from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.store.models import Document

from .serializers import DocumentSerializer


class DocumentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer
    model = Document
    queryset = model.objects.all()

    def get_queryset(self):
        # Owner
        return self.queryset.filter(owner_id=self.request.user.id)
