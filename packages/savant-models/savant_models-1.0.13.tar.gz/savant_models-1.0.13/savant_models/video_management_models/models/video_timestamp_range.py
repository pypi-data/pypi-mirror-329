from typing import Optional
from pydantic import BaseModel


class VideoTimeStampRange(BaseModel):

    start_time: Optional[int] = None
    end_time: Optional[int] = None

