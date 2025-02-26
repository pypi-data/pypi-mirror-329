from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from savant_models.profile_management_models.models.point import Point


class SkeletonPoints(BaseModel):
    points: Optional[List[Point]] = None
    model_config = ConfigDict(populate_by_name=True)

