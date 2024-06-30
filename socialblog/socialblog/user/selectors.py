from django.apps import apps
from django.db.models.query import QuerySet
from django.db.models import Q
from .models import BaseUser, Follow

from user.filters import BaseUserFilter




def user_get_login_data(*, user: BaseUser):
    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }


def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs



def get_following(user):
    return Follow.objects.filter(follower=user, status=Follow.STATUS.ACCEPTED).select_related('followed')

def get_followers(user):
    return Follow.objects.filter(followed=user, status=Follow.STATUS.ACCEPTED).select_related('follower')

def get_pending_follow_requests(user):
    return Follow.objects.filter(followed=user, status=Follow.STATUS.PENDING).select_related('follower')

def is_following(user, other_user):
    return Follow.objects.filter(follower=user, followed=other_user, status=Follow.STATUS.ACCEPTED).exists()

def follow_user(follower, followed):
    if not is_following(follower, followed):
        Follow.objects.create(follower=follower, followed=followed, status=Follow.STATUS.PENDING)

def unfollow_user(follower, followed):
    Follow.objects.filter(follower=follower, followed=followed).delete()

def accept_follow_request(followed, follower):
    follow_request = Follow.objects.filter(follower=follower, followed=followed, status=Follow.STATUS.PENDING).first()
    if follow_request:
        follow_request.status = Follow.STATUS.ACCEPTED
        follow_request.save()

def decline_follow_request(followed, follower):
    Follow.objects.filter(follower=follower, followed=followed, status=Follow.STATUS.PENDING).delete()

