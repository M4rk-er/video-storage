import redis
import os
from .models import Video
from vrc.settings import VIDEO_FILES_PATH, REDIS_HOST, REDIS_PORT


def get_redis_statuses(key, video_id):
    cache_key = f'video:{key}:{video_id}'
    redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))
    res = redis_client.get(cache_key)
    return res

# bool in redis, env
# delete file logic


def update_processing_and_status_in_redis(video_id, processing, status):

    processing_key = f'video:processing_status:{video_id}'
    status_key = f'video:last_processing_status:{video_id}'
    redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))
    redis_client.set(processing_key, processing)
    redis_client.set(status_key, status)


def update_videoname(video_id, new_filepath):

    video = Video.objects.get(pk=video_id)
    filename = os.path.basename(new_filepath)

    old_path = os.path.join(VIDEO_FILES_PATH, str(video.filepath))

    if os.path.exists(old_path):
        os.remove(old_path)

    video.filepath = 'video_files/' + os.path.basename(filename)
    video.save()


def get_new_filename(file_path, width, height):
    new_resolution = str(width) + 'x' + str(height)
    base_name, extension = os.path.splitext(file_path)
    base_name = base_name.rsplit('res-', 1)[0]
    new_filename = base_name + 'res-' + new_resolution + extension
    return new_filename


update_videoname('991a5001-a6bb-4ddb-bd9e-249bdff07f12', '/Users/bnovm/dev/OwnDev/video-storage/video_files/Playboi_Carti_-_H00DBYAIR_Official_Music_Video_L4odNaWres-900x600.mp4')
