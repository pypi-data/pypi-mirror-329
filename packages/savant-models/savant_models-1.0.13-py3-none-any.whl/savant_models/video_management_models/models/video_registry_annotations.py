from typing import List,Optional

from pydantic import BaseModel

from savant_models.video_management_models.models.video_registry_annotation import (
    VideoRegistryAnnotation,
)
from savant_models.video_management_models.models.video_registry_annotation_imported import VideoRegistryAnnotationImported


class VideoRegistryAnnotations(BaseModel):
    imported: Optional[List[VideoRegistryAnnotationImported]] = []
    phase: Optional[List[VideoRegistryAnnotation]] = []
    anatomy: Optional[List[VideoRegistryAnnotation]] = []
    instrument: Optional[List[VideoRegistryAnnotation]] = []
    triplet: Optional[List[VideoRegistryAnnotation]] = []
