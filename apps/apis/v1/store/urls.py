from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import DocumentViewSet

app_name = "store-v1"

router = SimpleRouter()

router.register(r"document", DocumentViewSet, basename="document")

urlpatterns = [
    path("", include(router.urls)),
]
