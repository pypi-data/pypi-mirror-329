from typing import Optional

from pydantic import ConfigDict

from savant_models.utils.base import BaseModel


class Point(BaseModel):
    sub_type: str
    color: Optional[str] = None
    count: Optional[int] = 1
    model_config = ConfigDict(populate_by_name=True)
