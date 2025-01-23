from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from common.models import BaseModel
# Create your models here.


class Notification(BaseModel):

    target = models.ForeignKey(setting)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.object_id

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"])
        ]

