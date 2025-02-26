from typing import List

from pydantic import BaseModel

from savant_models.utils.base import PyObjectId
from savant_models.sequence_management_models.models.analyser.annotation_error_metadata import AnnotationErrorMetadata


class AnnotationError(BaseModel):
    label_name: str
    number_of_encounters: int
    sequence_root_id: PyObjectId
    metadata: List[AnnotationErrorMetadata]
