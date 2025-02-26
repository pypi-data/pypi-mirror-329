from typing import List, Optional, Union

from pydantic import ConfigDict

from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.profile_management_models.models.shape import Shape
from savant_models.profile_management_models.models.tag_group import TagGroup
from savant_models.profile_management_models.enums.ml_model_enum import MLModelEnum


class ProfileObject(ProfileTag):
    # Specific to Profile
    shapes: Optional[List[Shape]] = []
    color: Optional[str] = None
    tags: Optional[List[ProfileTag]] = []
    group_tags: Optional[List[TagGroup]] = []
    count: Optional[int] = None
    ml_model: Optional[Union[MLModelEnum, str]] = MLModelEnum.SAM2

    model_config = ConfigDict(populate_by_name=True)
