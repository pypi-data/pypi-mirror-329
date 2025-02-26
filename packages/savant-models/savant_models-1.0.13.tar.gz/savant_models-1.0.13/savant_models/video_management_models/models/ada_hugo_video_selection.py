from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AdaHugoVideoSelection(BaseModel):
    aset_uuid: Optional[str] = None
    is_hugo: Optional[bool] = None
    video_origin: Optional[str] = None
    is_clinical: Optional[bool] = None
    has_user_interface: Optional[str] = None
    video_length: Optional[float] = None
    video_length_checks: Optional[str] = None
    fenestrated: Optional[bool] = None
    maryland: Optional[bool] = None
    contains_redactor_tags: Optional[bool] = None
    video_tag: Optional[str] = None
    comments: Optional[List[str]] = None
    ingested_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
