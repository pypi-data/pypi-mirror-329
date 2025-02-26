from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.utils.base import PyObjectId
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class TeamSummary(BaseModel):
    id: PyObjectId = Field(alias="_id")
    date_assigned: Optional[datetime] = None
    organisation_id: Optional[PyObjectId] = None
    name: str
    to_annotate: bool
    to_qa: bool
    to_review: bool
    to_fix: bool

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

