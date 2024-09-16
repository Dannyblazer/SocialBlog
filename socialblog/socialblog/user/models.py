import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from common.models import BaseModel
from common.utils import upload_location, default_image


class BaseUserManager(BUM):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        
        user = self.model(
            email=self.normalize_email(email.lower()),
            username=username,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )

        user.is_superuser = True
        user.is_admin=True
        user.save(using=self._db)

        return user

class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=100,
        unique=True,
    )
    username = models.CharField(
        verbose_name="username",
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="first_name",
        max_length=50,
        blank=True,
        null=True
        )
    last_name = models.CharField(
        verbose_name="last_name",
        max_length=50,
        blank=True,
        null=True
        )

    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    jwt_key = models.UUIDField(default=uuid.uuid4)

    objects = BaseUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return f"{self.username}"
    
    def is_staff(self):
        return self.is_admin
    


class Follow(BaseModel):
    class STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        DECLINED = "DECLINED", "Declined"

    follower = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='following_set')
    followed = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='followers_set')
    status = models.CharField(max_length=10, choices=STATUS.choices, default=STATUS.PENDING)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"


class Profile(BaseModel):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    image = models.ImageField(
        default=default_image,
        upload_to=upload_location,
        null=True, blank=True
    )
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)
