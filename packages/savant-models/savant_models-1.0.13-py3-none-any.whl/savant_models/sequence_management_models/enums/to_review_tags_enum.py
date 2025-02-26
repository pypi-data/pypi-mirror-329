from enum import StrEnum


class ToReviewTagsEnum(StrEnum):
    RANDOMLY_SELECTED = "Randomly Selected"
    MODEL_BASED_QA = "Model Based QA"
    RULE_BASED_QA = "Rule Based QA"
    ITERATIVE_QA = "Iterative QA"
