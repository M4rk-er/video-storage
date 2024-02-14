from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from videos.models import Video
from .serializers import VideoCreateSerializer, VideoSerializer


class VideoViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):

    queryset = Video.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return VideoCreateSerializer
        return VideoSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        try:
            video = Video.objects.create(**serializer.validated_data)
            video.save()
            details = {'id': video.id}
            return Response(details, status=status.HTTP_201_CREATED)

        except Exception as e:
            details = {'error': e}
            return Response(details, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):

        video = self.get_object()
        try:
            self.perform_destroy(video)
            Response({'succsess': True}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return {'error': e}
