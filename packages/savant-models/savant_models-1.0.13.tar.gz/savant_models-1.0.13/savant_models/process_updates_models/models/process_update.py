from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.utils.base import PyObjectId
from savant_models.process_updates_models.enums.user_type import UserType
from savant_models.process_updates_models.models.privilege import Privilege


class ProcessUpdate(BaseModel):
    update_id: PyObjectId = Field(alias="_id")

    update: str = Field(max_length=45)
    description: Optional[str] = None
    affected_users: List[UserType]
    affected_privileges: List[Privilege]
    date_released: datetime = datetime.now()

    model_config = ConfigDict(populate_by_name=True)

