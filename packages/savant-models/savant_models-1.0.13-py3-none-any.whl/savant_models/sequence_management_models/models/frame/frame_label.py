from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.profile_management_models.models.single_groupe_tag import SingleGroupTag
from savant_models.sequence_management_models.models.frame.label_shape import LabelShape
from savant_models.utils.base import PyObjectId
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class FrameLabel(BaseModel):  # FrameObject
    """Annotations are shapes with coordinates, label and tags."""

    id: PyObjectId = Field(alias="_id")
    code: str
    tags: Optional[List[ProfileTag]] = None
    shapes: Optional[List[LabelShape]] = []
    group_tags: Optional[List[SingleGroupTag]] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})
