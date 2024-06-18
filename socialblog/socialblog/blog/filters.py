import django_filters

from .models import Blog


class BlogFilter(django_filters.FilterSet):
    class Meta:
        model = Blog
        fields = ("id", "author", "title")
