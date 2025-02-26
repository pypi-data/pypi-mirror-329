from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.sequence_management_models.models.frame.frame_label import FrameLabel
from savant_models.utils.base import PyObjectId


class FrameEssential(BaseModel):
    """Whole annotation information in the database."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    # Actual annotations
    frame_path: Optional[str] = None
    labels: Optional[List[FrameLabel]] = []

    model_config = ConfigDict(populate_by_name=True)

