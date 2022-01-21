from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
    )
    list_display_links = ("id",)
    list_per_page = 100
