from datetime import datetime as python_datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel

from savant_models.utils.base import PyObjectId


class CommentResolve(BaseModel):
    resolved: Optional[bool] = False
    user_id: Optional[PyObjectId] = None
    user_name: Optional[str] = None
    sequence_id: Optional[PyObjectId] = None
    datetime: Optional[python_datetime] = None

    model_config = ConfigDict(populate_by_name=True)

