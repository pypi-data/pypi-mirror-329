from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdaVerifiedInstitutionCountry(BaseModel):
    surgeon_uuid: Optional[str] = None
    institution: Optional[str] = None
    country: Optional[str] = None
    ingested_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
