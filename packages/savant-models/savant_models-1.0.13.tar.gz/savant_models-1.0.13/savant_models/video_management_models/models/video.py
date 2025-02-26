from typing import List, Optional

from savant_models.video_management_models.models.deframer_job import DeframerJob
from savant_models.video_management_models.models.ada_metadata import AdaMetadata
from savant_models.video_management_models.models.video_registry_annotations import (
    VideoRegistryAnnotations,
)
from savant_models.video_management_models.models.video_summary import VideoSummary


class Video(VideoSummary):
    annotations: Optional[VideoRegistryAnnotations] = VideoRegistryAnnotations()
    deframer_jobs: Optional[List[DeframerJob]] = []
    ada_metadata: Optional[AdaMetadata] = None
