from django.core.serializers.python import Serializer

class LazyAccountEncoder(Serializer):
    def get_dump_objects(self, obj):
        dump_object = {}
        dump_object.update({'id': str(obj.pk)})
        dump_object.update({'username': str(obj.username)})
        dump_object.update({'profile_image': str(obj.profile.image.url)})
        return dump_object
    