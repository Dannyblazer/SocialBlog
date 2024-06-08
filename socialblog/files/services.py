import mimetypes
from typing import Any, Dict, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .enums import FileUploadStorage
from .models import File
from .utils import (
    bytes_to_mib,
)