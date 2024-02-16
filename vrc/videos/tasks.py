from videos.converter import change_video_resolution
from videos.utils import (update_processing_and_status_in_redis,
                          update_videoname)
from vrc.celery import app


@app.task
def resolution_change_task(video_id, file_path, new_filename, width, height,):

    update_processing_and_status_in_redis(video_id, int(True), int(False))
    try:
        change_video_resolution(file_path, new_filename, width, height)
        update_processing_and_status_in_redis(video_id, int(False), int(True))
        update_videoname(video_id, new_filename)

    except Exception:
        update_processing_and_status_in_redis(video_id, int(False), int(False))
