import logging
from datetime import datetime

from videos.converter import change_video_resolution
from videos.utils import (update_processing_and_status_in_redis,
                          update_videoname)
from vrc.celery import app

logger = logging.getLogger(__name__)


@app.task
def resolution_change_task(video_id, file_path, new_filename, width, height,):

    update_processing_and_status_in_redis(video_id, int(True))
    try:
        change_video_resolution(file_path, new_filename, width, height)
        update_processing_and_status_in_redis(video_id, int(False), int(True))
        update_videoname(video_id, new_filename)
        logger.info(
            f'{datetime.now().strftime("%H:%M:%S.%f")[:-5]} '
            f'- info: разрешение изменено'
        )

    except Exception as e:
        logger.error(
            f'{datetime.now().strftime("%H:%M:%S.%f")[:-5]} - error: {e}'
        )
        update_processing_and_status_in_redis(video_id, int(False), int(False))
