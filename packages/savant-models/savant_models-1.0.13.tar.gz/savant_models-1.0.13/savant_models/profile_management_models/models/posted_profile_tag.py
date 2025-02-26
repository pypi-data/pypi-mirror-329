from typing import Optional

from pydantic import ConfigDict, Field, field_validator

from savant_models.label_management_models.enums.label_category import LabelCategory
from savant_models.utils.base import BaseModel, PyObjectId
from savant_models.utils.validators.check_special_chars import check_special_chars


class PostedProfileTag(BaseModel):
    # From Label Registry
    id: PyObjectId = Field(alias="_id")
    code: Optional[str] = None
    display_name: Optional[str] = None
    category: Optional[LabelCategory] = None
    parent: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

    @field_validator('code', 'display_name', 'parent')
    def check_special_chars(cls, v: str):
        return check_special_chars(v)

