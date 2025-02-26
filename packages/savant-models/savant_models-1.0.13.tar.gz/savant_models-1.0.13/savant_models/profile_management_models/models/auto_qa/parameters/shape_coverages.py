from typing import List

from pydantic import BaseModel

from savant_models.profile_management_models.models.auto_qa.shape_coverage import ShapeCoverage


class ShapeCoverages(BaseModel):
    shape_coverages: List[ShapeCoverage]
