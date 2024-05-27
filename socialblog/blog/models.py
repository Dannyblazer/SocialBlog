from django.db import models
from django.utils import timezone

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(BaseModel):
    title = models.CharField(max_length=50)
    body  = models.TextField()


    def __str__(self):
        return f"{self.title}"