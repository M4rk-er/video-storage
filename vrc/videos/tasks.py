from vrc.celery import app
from videos.converter import change_video_resolution
from videos.utils import update_videoname, update_processing_and_status_in_redis


@app.task
def resolution_change_task(video_id, file_path, new_filename, width, height,):

    update_processing_and_status_in_redis(video_id, 'true', 'false')
    try:
        change_video_resolution(file_path, new_filename, width, height)
        update_processing_and_status_in_redis(video_id, 'false', 'true')
        update_videoname(video_id, new_filename)

    except Exception:
        update_processing_and_status_in_redis(video_id, 'false', 'false')
