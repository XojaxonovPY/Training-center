from rest_framework.serializers import ModelSerializer

from apps.models import Media


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = 'image',
