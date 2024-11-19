from django.contrib import admin

# Register your models here.
from .models import BaseUser

admin.site.register(BaseUser)