import logging
import os

import redis

from vrc.settings import REDIS_HOST, REDIS_PORT, VIDEO_FILES_PATH

from .models import Video

logger = logging.getLogger(__name__)


def get_redis_statuses(key, video_id):
    cache_key = f'video:{key}:{video_id}'
    redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))
    res = redis_client.get(cache_key)
    if res:
        return int(res) == 1
    return res


def update_processing_and_status_in_redis(video_id, processing, status=None):

    processing_key = f'video:processing_status:{video_id}'
    status_key = f'video:last_processing_status:{video_id}'
    redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))
    redis_client.set(processing_key, processing)
    if status:
        redis_client.set(status_key, status)


def delete_file_if_exists(filepath):

    if os.path.exists(filepath):
        os.remove(filepath)
        logger.info(f'файл - {filepath} удален')
        return True

    logger.info(f'файл - {filepath} не найден')
    return False


def update_videoname(video_id, new_filepath):

    video = Video.objects.get(pk=video_id)
    filename = os.path.basename(new_filepath)

    old_path = os.path.join(VIDEO_FILES_PATH, str(video.filepath))
    delete_file_if_exists(old_path)

    video.filepath = 'video_files/' + os.path.basename(filename)
    video.save()


def get_new_filename(file_path, width, height):
    new_resolution = str(width) + 'x' + str(height)
    base_name, extension = os.path.splitext(file_path)
    base_name = base_name.rsplit('-res-', 1)[0]
    new_filename = base_name + '-res-' + new_resolution + extension
    return new_filename
