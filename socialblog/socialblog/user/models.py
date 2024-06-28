import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from common.models import BaseModel
from common.utils import upload_location, default_image
# Create your models here.

# The BaseUserManager
class BaseUserManager(BUM):
    """ The create user method on the for the BaseUserManager """
    def create_user(self, email, username, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email.lower()),
            username=username,
            is_active=is_active,
            is_admin=is_admin,
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
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user
    

class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    """ The Base User inheriting Other classes to form the complete user model """
    email = models.EmailField(
        verbose_name="email address",
        max_length=100,
        unique=True,
    )
    username = models.CharField(
        verbose_name="username",
        max_length=100,
        unique=True,
    )

    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    # This should potentially be an encrypted field
    jwt_key = models.UUIDField(default=uuid.uuid4)

    objects = BaseUserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.username}"
    
    # staff boolean method
    def is_staff(self):
        return self.is_admin
    

class Profile(models.Model):
    """ User Profile Class hooked to the User model """
    user    = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    image   = models.ImageField(
                default=default_image,
                upload_to=upload_location,
                null=True, blank=True) # Remember to remove the null after default image is set
    
    bio     = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)

