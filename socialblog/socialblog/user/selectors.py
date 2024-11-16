from django.apps import apps
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import BaseUser, Follow

from user.filters import BaseUserFilter
from django.db import transaction



def user_get_login_data(*, user: BaseUser):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }


def user_get(user_id) -> BaseUser:
    return get_object_or_404(BaseUser, pk=user_id)


def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs


def get_following(user) -> QuerySet[Follow]:
    return Follow.objects.filter(follower=user, status=Follow.STATUS.PENDING).select_related('followed')


def get_followers(user) -> QuerySet[Follow]:
    return Follow.objects.filter(followed=user, status=Follow.STATUS.PENDING).select_related('follower')


def get_pending_follow_requests(user) -> QuerySet[Follow]:
    return Follow.objects.filter(followed=user, status=Follow.STATUS.PENDING).select_related('follower')


def is_following(user, other_user) -> bool:
    return Follow.objects.filter(follower=user, followed=other_user).exists()


def follow_user(follower, followed):
    if not is_following(follower, followed):
        Follow.objects.create(follower=follower, followed=followed, status=Follow.STATUS.PENDING)
        return True
    return False


def unfollow_user(follower, followed):
    if is_following(follower, followed):
        Follow.objects.filter(follower=follower, followed=followed).delete()
        return True
    return False


def accept_follow_request(request_id):
    """
    Accept a follow request.
    """
    follow_request = get_object_or_404(Follow, pk=request_id)
    
    if follow_request.status == Follow.STATUS.ACCEPTED:
        return False  # Request is already accepted

    with transaction.atomic():
        follow_request.status = Follow.STATUS.ACCEPTED
        follow_request.save()

    return True


def decline_follow_request(request_id: int) -> bool:
    """
    Decline a follow request.
    """
    follow_request = get_object_or_404(Follow, pk=request_id, status=Follow.STATUS.PENDING)
    follow_request.delete()
    return True

    # follow_request = get_object_or_404(Follow, pk=request_id, status=Follow.STATUS.PENDING)
    # follow_request.delete()

