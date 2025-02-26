from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict

from savant_models.utils.base import BaseModel, PyObjectId


class VersionHistory(BaseModel):
    version: str
    profile_id: PyObjectId
    date: datetime
    tags: Optional[List[str]] = []
    description: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)
