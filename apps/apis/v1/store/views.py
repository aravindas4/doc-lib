from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.store.models import Document, User

from .serializers import (
    DocumentSerializer,
    StringListSerializer,
    UserSerializer,
)


class DocumentViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocumentSerializer
    model = Document
    queryset = model.objects.all()

    def get_queryset(self):
        if self.action in ["list", "retrieve", "partial_update"]:
            # Owner or Shared User
            return self.queryset.filter(
                Q(owner_id=self.request.user.id)
                | Q(shared_users__id=self.request.user.id)
            )
        # Owner
        return self.queryset.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        # Saving the owner of the document
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        """Overridden to track the api caller."""
        context = super().get_serializer_context()
        context["api_caller"] = self.request.user
        return context

    @action(methods=["POST"], detail=True, url_path="share")
    def share(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StringListSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        instance.add_shared_users(serializer.validated_data["id_list"])
        return self.retrieve(request, *args, **kwargs)


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    model = User
    queryset = model.objects.all()
