from typing import Optional
from django.db import transaction

from.models import Blog
from common.services import model_update
from user.models import BaseUser



def blog_create(
    *, author: BaseUser, title: str, body: str, like: int
) -> Blog:
    blog = Blog.objects.create(author=author, title=title, body=body, like=like)

    return blog


@transaction.atomic
def blog_update(*, blog: Blog, data) -> Blog:
    non_side_effect_fields = ["title", "body", "like"]

    user, has_updated = model_update(instance=blog, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user