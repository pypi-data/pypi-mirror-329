from datetime import datetime
from typing import List

from pydantic import BaseModel

from savant_models.sequence_management_models.models.video.video_annotation import VideoAnnotation
from savant_models.utils.base import PyObjectId


class VideoRegistryAnnotation(BaseModel):
    date: datetime
    project_id: PyObjectId
    project_name: str
    batch_id: PyObjectId
    root_id: PyObjectId
    video_annotations: List[VideoAnnotation]

