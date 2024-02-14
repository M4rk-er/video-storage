from rest_framework import serializers
from videos.models import Video


class VideoCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, write_only=True)

    class Meta:
        model = Video
        fields = ('file',)


class VideoSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id', 'filename')
    
    def get_filename(self, video):
        return video.filename
