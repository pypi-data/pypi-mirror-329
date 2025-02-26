from typing import List

from pydantic import BaseModel

from savant_models.profile_management_models.models.auto_qa.label_to_relative_labels import LabelToRelativeLabels


class LabelsToRelativeLabels(BaseModel):
    labels_to_relative_labels: List[LabelToRelativeLabels]
