from rest_framework import serializers

from videos.models import Video
from videos.utils import get_redis_statuses

from .validators import validate_file_type, validate_res_field


class VideoCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True,
                                 write_only=True,
                                 source='filepath',
                                 validators=[validate_file_type],)

    class Meta:
        model = Video
        fields = ('file',)


class VideoSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    processing = serializers.SerializerMethodField()
    processing_success = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id', 'filename', 'processing', 'processing_success')

    def get_filename(self, video):
        return video.filename

    def get_processing(self, video):
        video_id = video.pk
        return get_redis_statuses('processing_status', video_id)

    def get_processing_success(self, video):
        video_id = video.pk
        return get_redis_statuses('last_processing_status', video_id)


class VideoResolutionSerializer(serializers.Serializer):
    width = serializers.IntegerField(validators=[validate_res_field])
    height = serializers.IntegerField(validators=[validate_res_field])
