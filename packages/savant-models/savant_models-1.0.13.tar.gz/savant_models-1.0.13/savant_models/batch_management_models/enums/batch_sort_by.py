from enum import StrEnum


class BatchSortBy(StrEnum):
    SEQUENCE_COUNT = "sequence_count"
    FRAME_COUNT = "frame_count"
    VIDEO_COUNT = "video_count"
    DUE_DATE = "due_date"
    TO_FIX_DUE_DATE = "to_fix_due_date"
    DATE_CREATED = "date_created"
    TO_ANNOTATE = "to_annotate"
    TO_QA = "to_qa"
    TO_REVIEW = "to_review"
    TO_FIX = "to_fix"
    COMPLETED = "completed"
