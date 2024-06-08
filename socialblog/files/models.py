from django.conf import settings
from django.db import models

from common.models import BaseModel
from .enums import FileUploadStorage
from .utils import file_generate_upload_path
from user.models import BaseUser
# Create your models here.


class File(BaseModel):
    file = models.FileField(
            upload_to=file_generate_upload_path,
            blank=True,
            null=True)
    orginal_file_name = models.TextField()
    file_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=50)

    # Delete files too
    uploaded_by = models.ForeignKey(BaseUser, null=True, on_delete=models.CASCADE)
    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        """
        We consider a file 'valid' if the datetime flag has a value
        """
        return bool(self.upload_finished_at)
    
    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.S3:
            return self.file.url
        
        return f"{settings.APP_DOMAIN}{self.file.url}"

