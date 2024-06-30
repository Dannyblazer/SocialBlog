from typing import Optional

from django.db import transaction

from common.services import model_update
from user.models import BaseUser


def user_create(
    *, email: str, username: str, password: Optional[str] = None
) -> BaseUser:
    user = BaseUser.objects.create_user(email=email, username=username, password=password)

    return user


@transaction.atomic
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields = ["email", "username"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
