from enum import StrEnum


class SequenceStatus(StrEnum):
    TO_ANNOTATE = "to_annotate"
    TO_QA = "to_qa"
    TO_FIX = "to_fix"
    TO_REVIEW = "to_review"
    COMPLETED = "completed"
