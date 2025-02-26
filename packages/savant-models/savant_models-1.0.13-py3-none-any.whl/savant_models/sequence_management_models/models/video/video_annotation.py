from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.profile_management_models.models.single_groupe_tag import SingleGroupTag
from savant_models.utils.base import PyObjectId


class VideoAnnotation(BaseModel):
    id: PyObjectId = Field(alias="_id")
    timestamp_start: float
    timestamp_end: float
    label: Optional[ProfileTag] = None
    description: Optional[str] = None
    color: str
    tags: Optional[List[ProfileTag]] = []
    group_tags: Optional[List[SingleGroupTag]] = []
    annotated_by: PyObjectId
    date_annotated: datetime
    locked: Optional[bool] = False

    model_config = ConfigDict(populate_by_name=True)

