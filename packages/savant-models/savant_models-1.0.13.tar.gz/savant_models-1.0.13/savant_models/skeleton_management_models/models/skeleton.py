from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, Field

from savant_models.profile_management_models.models.link import Link
from savant_models.profile_management_models.models.point import Point
from savant_models.utils.base import BaseModel, PyObjectId
from savant_models.skeleton_management_models.enums.skeleton_type import SkeletonType
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class Skeleton(BaseModel):
    id: PyObjectId = Field(alias="_id")

    name: str
    color: str
    points: List[Point]
    links: Optional[List[Link]] = []
    creator_id: Optional[PyObjectId] = None
    date_created: Optional[datetime] = None
    type: Optional[SkeletonType] = SkeletonType.SKELETON
    organisation_id: Optional[PyObjectId] = None
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

