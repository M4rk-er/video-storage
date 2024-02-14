import uuid
import os

from django.db import models


class Video(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    file = models.FileField(
        upload_to='video_files/'
    )

    @property
    def filename(self):
        return os.path.basename(self.file.name)
