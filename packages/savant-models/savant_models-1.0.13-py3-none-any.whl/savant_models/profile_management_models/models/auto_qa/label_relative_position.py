from typing import List, Optional

from pydantic import BaseModel

from savant_models.profile_management_models.enums.auto_qa.comparison_type import ComparisonType
from savant_models.profile_management_models.enums.auto_qa.relative_position import RelativePosition


class LabelRelativePosition(BaseModel):
    label_code: str
    relative_position: List[RelativePosition]
    comparison_type: Optional[ComparisonType] = ComparisonType.CENTRE_POINT
