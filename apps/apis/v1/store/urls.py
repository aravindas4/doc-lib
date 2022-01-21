from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import DocumentViewSet, UserViewSet

app_name = "store-v1"

router = SimpleRouter()

router.register(r"document", DocumentViewSet, basename="document")
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
