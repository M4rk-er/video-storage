from rest_framework import routers
from django.urls import include, path

from .views import VideoViewset

app_name = 'api'

router = routers.DefaultRouter()
router.register('videos', VideoViewset)


urlpatterns = [
    path('', include(router.urls)),
]
