from datetime import datetime

from pydantic import BaseModel


class S3FileProject(BaseModel):

    name: str
    size: int
    date_uploaded: datetime
