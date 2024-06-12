from django.contrib import admin

# Register your models here.
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        #"original_file_name",
        "file_name",
        "file_type",
        "url",
        "uploaded_by",
        "created_at",
        "upload_finished_at",
        "is_valid",
    ]
    list_select_related = ["uploaded_by"]

    ordering = ["-created_at"]
