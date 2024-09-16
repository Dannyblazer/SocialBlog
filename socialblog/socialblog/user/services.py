from typing import Optional

from django.db import transaction

from common.services import model_update
from user.models import BaseUser, Profile


def user_create(
    *, email: str, username: str, password: Optional[str] = None
) -> BaseUser:
    user = BaseUser.objects.create_user(email=email, username=username, password=password)
    
    Profile.objects.create(user=user) # REMEMBER TO CELERIZE THIS!

    return user


@transaction.atomic
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields = ["email", "username"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user

@transaction.atomic
def profile_update(*, profile: Profile, data) -> Profile:
    non_side_effect_fields = ["image", "bio", "location", "birth_date"]

    user, has_updated = model_update(instance=profile, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user