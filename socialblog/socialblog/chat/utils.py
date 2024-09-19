from django.contrib.humanize.templatetags.humanize import naturalday
#from django.core.serializers.python import Serializer
from datetime import datetime
from django.utils.timezone import localtime

def calculate_timestamp(timestamp):
    """
    Convert the timestamp using humanize to something nice
    """
    local_timestamp = localtime(timestamp)  # Convert to the local timezone (e.g., Africa/Lagos)

    # Today or Yesterday
    if ((naturalday(local_timestamp) == "today") or (naturalday(local_timestamp) == "yesterday")):
        str_time = datetime.strftime(local_timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        ts = f"{naturalday(local_timestamp)} at {str_time}"

    # Other day
    else:
        str_time = datetime.strftime(local_timestamp, "%m/%d/%Y")
        ts = f"{str_time}"
    
    return str(ts)
