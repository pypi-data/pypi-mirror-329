from enum import StrEnum


class AnnotationErrorReasonEnum(StrEnum):
    REMOVED = "removed"
    ADDED = "added"
    EDITED = "edited"
