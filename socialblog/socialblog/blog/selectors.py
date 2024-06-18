from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from .models import Blog
from .filters import BlogFilter


def blog_list(*, filters=None) -> QuerySet[Blog]:
    filters = filters or {}

    qs = Blog.objects.all()

    return BlogFilter(filters, qs).qs


def blog_get(blog_id):
    return get_object_or_404(Blog, pk=blog_id)
