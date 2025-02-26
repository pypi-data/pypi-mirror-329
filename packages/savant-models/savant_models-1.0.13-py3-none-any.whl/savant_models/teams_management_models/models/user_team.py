from typing import Optional

from pydantic import ConfigDict, BaseModel

from savant_models.utils.base import PyObjectId
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class UserTeam(BaseModel):
    id: PyObjectId
    name: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

