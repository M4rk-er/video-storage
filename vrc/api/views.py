from rest_framework.viewsets import ModelViewSet

from videos.models import Video
from .serializers import VideoCreateSerializer, VideoSerializer


class VideoViewset(ModelViewSet):
    queryset = Video.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return VideoCreateSerializer
        return VideoSerializer
