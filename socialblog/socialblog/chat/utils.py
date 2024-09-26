from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.serializers.python import Serializer
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


base_url = 'https://taskitly.com'

class LaxyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        #dump_object.update({"msg_type": MSG_TYPE_MESSAGE})
        dump_object.update({"msg_id": str(obj.id)})
        dump_object.update({"user_id": str(obj.sender.pk)})
        dump_object.update({"username": str(obj.sender.username)})
        dump_object.update({"message": str(obj.content)})
        dump_object.update({"profile_image": f"{base_url}{str(obj.sender.profile.image.url)}"})
        dump_object.update({"natural_timestamp": calculate_timestamp(obj.created_at)})
        return dump_object

