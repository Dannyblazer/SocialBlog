from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from blog.models import Blog, Like
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "title", "created_at", "updated_at"]
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request)
    

@admin.register(Like)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "blog"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request)