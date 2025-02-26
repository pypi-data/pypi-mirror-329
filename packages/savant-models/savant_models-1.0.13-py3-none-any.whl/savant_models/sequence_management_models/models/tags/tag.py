from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.utils.base import PyObjectId


class Tag(BaseModel):
    id: PyObjectId = Field(alias="_id")

    datetime_created: Optional[datetime] = datetime.now()
    creator_id: Optional[PyObjectId] = None
    label: Optional[str] = None
    active: Optional[bool] = True

    model_config = ConfigDict(populate_by_name=True)

