from pydantic import BaseModel

from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.utils.base import PyObjectId


class AnnotationErrorMetadata(BaseModel):
    frame_index_identified: int
    status_error_identified: SequenceStatus
    sequence_id: PyObjectId
