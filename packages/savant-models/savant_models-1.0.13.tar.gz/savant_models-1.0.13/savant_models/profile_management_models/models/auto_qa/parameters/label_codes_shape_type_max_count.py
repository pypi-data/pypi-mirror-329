from typing import Optional

from savant_models.profile_management_models.enums.auto_qa.shape_type import ShapeType
from savant_models.profile_management_models.models.auto_qa.parameters.label_codes import LabelCodes


class LabelCodesShapeTypeMaxCount(LabelCodes):
    shape_type: ShapeType
    max_count: Optional[int] = None
