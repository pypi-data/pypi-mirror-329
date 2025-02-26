from typing import List

from pydantic import BaseModel

from savant_models.profile_management_models.models.auto_qa.section_label_min_max_count import SectionLabelMinMaxCount


class SectionLabelCount(BaseModel):
    section_label_counts: List[SectionLabelMinMaxCount]
