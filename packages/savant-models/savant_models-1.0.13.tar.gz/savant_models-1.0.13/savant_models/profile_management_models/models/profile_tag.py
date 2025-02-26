from typing import Optional

from pydantic import ConfigDict, Field

from savant_models.label_management_models.enums.label_category import LabelCategory
from savant_models.utils.base import BaseModel, PyObjectId


class ProfileTag(BaseModel):
    # From Label Registry
    id: PyObjectId = Field(alias="_id")
    code: str
    display_name: str
    category: LabelCategory
    parent: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)

