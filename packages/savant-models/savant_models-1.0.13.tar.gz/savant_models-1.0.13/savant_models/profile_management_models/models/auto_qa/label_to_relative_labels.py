from typing import List, Union

from pydantic import BaseModel

from savant_models.profile_management_models.models.auto_qa.label_relative_position import LabelRelativePosition
from savant_models.profile_management_models.models.auto_qa.label_relative_size import LabelRelativeSize


class LabelToRelativeLabels(BaseModel):
    label_code: str
    relative_labels: Union[List[LabelRelativeSize], List[LabelRelativePosition]]
