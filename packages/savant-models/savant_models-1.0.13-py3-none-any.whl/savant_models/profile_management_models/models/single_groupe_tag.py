from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from savant_models.utils.base import PyObjectId
from savant_models.profile_management_models.models.posted_profile_tag import PostedProfileTag


class SingleGroupTag(BaseModel):
    skeleton_id: PyObjectId
    name: Optional[str] = None
    tags: Optional[List[PostedProfileTag]] = []

    model_config = ConfigDict(populate_by_name=True)

