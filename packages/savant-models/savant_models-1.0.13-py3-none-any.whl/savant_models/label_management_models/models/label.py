from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field

from savant_models.label_management_models.enums.label_category import LabelCategory
from savant_models.utils.base import BaseModel, PyObjectId


class Label(BaseModel):
    id: PyObjectId = Field(alias="_id")
    code: str
    display_name: str
    parent: Optional[str] = None
    category: LabelCategory
    date_created: datetime
    creator_id: PyObjectId
    organisation_id: Optional[PyObjectId] = None
    model_config = ConfigDict(populate_by_name=True)

