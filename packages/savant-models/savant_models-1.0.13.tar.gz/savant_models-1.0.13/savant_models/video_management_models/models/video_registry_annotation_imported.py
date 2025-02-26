from datetime import datetime
from typing import List

from pydantic import BaseModel

from savant_models.sequence_management_models.models.video.video_annotation import VideoAnnotation


class VideoRegistryAnnotationImported(BaseModel):
    date: datetime
    layer_id: str
    video_annotations: List[VideoAnnotation]
