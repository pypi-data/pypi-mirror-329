from typing import Optional

from pydantic import BaseModel

from savant_models.video_management_models.models.ada_hugo_video_selection import AdaHugoVideoSelection
from savant_models.video_management_models.models.ada_verified_institution_country import (
    AdaVerifiedInstitutionCountry,
)


class AdaMetadata(BaseModel):
    hugo_video_selection: Optional[AdaHugoVideoSelection] = AdaHugoVideoSelection()
    verified_institution_country: Optional[AdaVerifiedInstitutionCountry] = (
        AdaVerifiedInstitutionCountry()
    )
