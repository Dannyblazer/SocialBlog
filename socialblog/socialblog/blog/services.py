from typing import Optional
from django.db import transaction

from.models import Blog, Comment
from common.services import model_update
from user.models import BaseUser



def blog_create(
    *, author: BaseUser, title: str, body: str
) -> Blog:
    blog = Blog.objects.create(author=author, title=title, body=body)

    return blog


@transaction.atomic
def blog_update(*, blog: Blog, data) -> Blog:
    non_side_effect_fields = ["title", "body", "like"]

    user, has_updated = model_update(instance=blog, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user, has_updated



def comment_create(
    *, owner: BaseUser, post: Blog, body: str
) -> Blog:
    comment = Comment.objects.create(owner=owner, post=post, body=body)

    return comment
