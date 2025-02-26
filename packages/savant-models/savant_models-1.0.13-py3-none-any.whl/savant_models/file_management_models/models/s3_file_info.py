from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class S3FileInfo(BaseModel):
    key: str
    last_modified: Optional[datetime] = None
