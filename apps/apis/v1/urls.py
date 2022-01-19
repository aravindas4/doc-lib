from django.urls import include, path

from .store import urls as store_urls

urlpatterns = [
    path("store/", include(store_urls)),
]
