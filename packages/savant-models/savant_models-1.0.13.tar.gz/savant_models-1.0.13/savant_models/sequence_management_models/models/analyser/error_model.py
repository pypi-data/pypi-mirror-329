from typing import List, Optional

from pydantic import BaseModel

from savant_models.sequence_management_models.models.analyser.annotation_error import AnnotationError


class ErrorModel(BaseModel):
    major: Optional[List[AnnotationError]] = None
    minor: Optional[List[AnnotationError]] = None
    patch: Optional[List[AnnotationError]] = None
