from email.quoprimime import body_check
from django.db import models
#from django.utils import timezone
from common.models import BaseModel
from django.conf import settings
# Create your models here.


class Blog(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=100)
    body  = models.TextField()


    def __str__(self):
        return f"{self.title}"


class Comment(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment')
    post  = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    body  = models.TextField()

    def __str__(self):
        return f"{self.owner}"
    

class Like(BaseModel):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, related_name='likes')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_blogs')

    def __str__(self):
        return f"Likes for {self.blog.title}"
