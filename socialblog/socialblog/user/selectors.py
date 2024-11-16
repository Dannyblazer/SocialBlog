from django.apps import apps
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import BaseUser, Follow

from user.filters import BaseUserFilter




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
    if follower != followed:
        if not is_following(follower, followed):
            Follow.objects.create(follower=follower, followed=followed, status=Follow.STATUS.PENDING)
            return True
    return False


def unfollow_user(follower, followed):
    if is_following(follower, followed):
        Follow.objects.filter(follower=follower, followed=followed).delete()
        return True
    return False


def accept_follow_request(user, request_id):
    # A better fix would be to include the authenticated user(user) in the follow request query but that'll be later
    follow_request = get_object_or_404(Follow, pk=request_id)
    if user != follow_request.follower:
        if follow_request.status != Follow.STATUS.ACCEPTED:
            follow_request.status = Follow.STATUS.ACCEPTED
            follow_request.save()
            return True
    return False


def decline_follow_request(user, request_id):
    # A better fix would be to include the authenticated user(user) in the follow request query but that'll be later
    follow_request = get_object_or_404(Follow, pk=request_id, status=Follow.STATUS.PENDING)
    if user == follow_request.followed:
        follow_request.delete()
        return True
    return False

