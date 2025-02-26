from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.sequence_management_models.models.comments.comment import Comment
from savant_models.sequence_management_models.models.frame.frame_label import FrameLabel
from savant_models.utils.base import PyObjectId


class Frame(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    # Actual annotations
    seen: Optional[bool] = False
    comment_count: Optional[int] = 0
    comments: Optional[List[Comment]] = []
    frame_path: Optional[str] = None
    labels: Optional[List[FrameLabel]] = []
    annotated_by: Optional[PyObjectId] = None
    date_annotated: Optional[datetime] = None
    tags: Optional[List[ProfileTag]] = []
    timestamp: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)

