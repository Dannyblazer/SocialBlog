from django.db import models
#from django.utils import timezone
from common.models import BaseModel
# Remember to change this user model import from settings
from django.conf import settings
# Create your models here.


class Blog(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=50)
    body  = models.TextField()


    def __str__(self):
        return f"{self.title}"