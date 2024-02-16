import os
import uuid

from django.db import models


class Video(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    filepath = models.FileField(
        upload_to='video_files/',
        max_length=1024
    )

    @property
    def filename(self):
        return os.path.basename(self.filepath.name)
