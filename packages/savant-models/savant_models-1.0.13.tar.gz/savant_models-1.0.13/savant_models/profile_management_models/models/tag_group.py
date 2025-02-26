from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from savant_models.utils.base import PyObjectId
from savant_models.profile_management_models.models.profile_tag import ProfileTag

class TagGroup(BaseModel):
    skeleton_id: PyObjectId
    required: bool
    multi_select: bool
    name: Optional[str] = None
    tags: Optional[List[ProfileTag]] = []
    model_config = ConfigDict(populate_by_name=True)

