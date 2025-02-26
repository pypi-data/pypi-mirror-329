from typing import List

from pydantic import field_validator

from savant_models.profile_management_models.models.auto_qa.parameters.label_codes import LabelCodes
from savant_models.sequence_management_models.models.frame.shape_point import ShapePoint


class LabelCodesRegion(LabelCodes):
    region: List[ShapePoint]

    @field_validator('region')
    @classmethod
    def validate_region(cls, value: List[ShapePoint]):
        if len(value) != 2:
            raise ValueError(f"Region must have exactly 2 points")

        if not all(0 <= point.x <= 1 and 0 <= point.y <= 1 for point in value):
            raise ValueError(f"Region points must be in the range [0, 1]")

        return value
