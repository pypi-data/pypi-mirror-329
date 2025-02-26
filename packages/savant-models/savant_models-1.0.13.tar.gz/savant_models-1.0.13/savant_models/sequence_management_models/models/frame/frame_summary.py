from typing import Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.utils.base import PyObjectId


class FrameSummary(BaseModel):
    """Whole annotation information in the database."""
    id: PyObjectId = Field(alias="_id")

    # Actual annotations
    frame_path: Optional[str] = None

    timestamp: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)

