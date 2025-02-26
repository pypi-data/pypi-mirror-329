from typing import Optional

from pydantic import ConfigDict, BaseModel
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class FrameImageSize(BaseModel):  # FrameObject
    x: Optional[int] = 900
    y: Optional[int] = 600

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})
