from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .filters import BlogFilter


def blog_list(*, filters=None) -> QuerySet[Blog]:
    filters = filters or {}
    qs = Blog.objects.select_related('author')
    return BlogFilter(filters, qs).qs


def blog_get(blog_id) -> Blog:
    return get_object_or_404(Blog, pk=blog_id)


def comment_list(blog_id: int) -> QuerySet[Blog]:
    qs = Blog.objects.prefetch_related('comments').get(pk=blog_id)
    return qs.comments.all()


def comment_get(comment_id) -> Comment:
    return get_object_or_404(Comment, pk=comment_id)

