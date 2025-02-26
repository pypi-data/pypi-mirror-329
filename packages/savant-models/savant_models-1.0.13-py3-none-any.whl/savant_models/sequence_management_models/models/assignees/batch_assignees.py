from typing import Optional, List

from pydantic import ConfigDict, BaseModel

from savant_models.utils.base import PyObjectId
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class BatchAssignees(BaseModel):  # FrameObject
    """Annotations are shapes with coordinates, label and tags."""
    to_annotate: Optional[List[PyObjectId]] = []
    to_qa: Optional[List[PyObjectId]] = []
    to_fix: Optional[List[PyObjectId]] = []

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

