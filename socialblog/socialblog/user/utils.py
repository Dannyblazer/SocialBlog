from django.core.serializers.python import Serializer

class LazyAccountEncoder(Serializer):
    def get_dump_objects(self, obj):
        dump_object = {
            'id': str(obj.pk),
            'username': str(obj.username),
            'profile_image': str(obj.profile.image.url) if obj.profile.image else None
        }
        return dump_object
