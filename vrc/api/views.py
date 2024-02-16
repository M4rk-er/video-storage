from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from videos.models import Video
from videos.tasks import resolution_change_task
from videos.utils import delete_file_if_exists, get_new_filename

from .serializers import (VideoCreateSerializer,
                          VideoResolutionSerializer,
                          VideoSerializer,)


class VideoViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):

    queryset = Video.objects.all()
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):

        if self.request.method in ['POST']:
            return VideoCreateSerializer

        if self.request.method in ['PATCH']:
            return VideoResolutionSerializer

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

            is_delete = delete_file_if_exists(video.filepath.path)
            if is_delete:
                self.perform_destroy(video)
                data = {'succsess': True}
                return Response(data, status=status.HTTP_204_NO_CONTENT)

            data = {'error': 'Файл не существует'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            data = {'error': e}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        video = self.get_object()
        width = serializer.validated_data.get('width')
        height = serializer.validated_data.get('height')
        new_filename = get_new_filename(video.filepath.path, width, height)

        try:
            resolution_change_task.delay(
                video.pk, video.filepath.path, new_filename, width, height
            )
            data = {'succsess': True}
            return Response(data, status=status.HTTP_200_OK)

        except Exception:
            data = {'succsess': False}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
