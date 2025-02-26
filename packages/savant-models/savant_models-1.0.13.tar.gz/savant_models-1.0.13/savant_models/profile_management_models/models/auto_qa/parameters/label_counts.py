from typing import List

from pydantic import BaseModel

from savant_models.profile_management_models.models.auto_qa.label_min_max_count import LabelMinMaxCount


class LabelCounts(BaseModel):
    label_counts: List[LabelMinMaxCount]
