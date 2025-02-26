from pydantic import ConfigDict

from savant_models.utils.base import BaseModel
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class OptionResponse(BaseModel):
    option: str
    response: bool

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})
