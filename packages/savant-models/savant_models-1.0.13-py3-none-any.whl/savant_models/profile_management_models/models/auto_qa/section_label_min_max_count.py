from savant_models.profile_management_models.models.auto_qa.label_min_max_count import LabelMinMaxCount


class SectionLabelMinMaxCount(LabelMinMaxCount):
    section_start: int
    section_end: int
