from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel

from savant_models.utils.base import PyObjectId
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class Assignee(BaseModel):  # FrameObject
    """Annotations are shapes with coordinates, label and tags."""
    date_assigned: Optional[datetime] = None
    user_id: PyObjectId
    name: Optional[str] = None
    team_id: Optional[PyObjectId] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

