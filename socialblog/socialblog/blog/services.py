#from typing import Optional
#from xmlrpc.client import Boolean
from django.db import transaction

from.models import Blog, Comment, Like
from common.services import model_update
from user.models import BaseUser



def blog_create(
    *, author: BaseUser, title: str, body: str
) -> Blog:

    return Blog.objects.create(author=author, title=title, body=body)


@transaction.atomic
def blog_update(*, blog: Blog, data) -> Blog:
    non_side_effect_fields = ["title", "body"]

    user, has_updated = model_update(instance=blog, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user


def blog_delete(blog):
    blog.delete()


def comment_create(
    *, owner: BaseUser, post: Blog, body: str
) -> Blog:

    return Comment.objects.create(owner=owner, post=post, body=body)

@transaction.atomic
def blog_like(user: BaseUser, blog: Blog) -> bool:
    like, created = Like.objects.get_or_create(blog=blog)
    if not like.users.filter(email=user.email).exists():
        like.users.add(user)
        like.full_clean()
        like.save()
        return True
    return False

def comment_delete(comment):
    comment.delete()