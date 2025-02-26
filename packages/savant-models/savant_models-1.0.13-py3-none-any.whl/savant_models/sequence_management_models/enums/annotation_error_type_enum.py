from enum import StrEnum


class AnnotationErrorTypeEnum(StrEnum):
    MAJOR = "major"  # Shape/object added
    MINOR = "minor"  # Shape/Object removed
    PATCH = "patch"  # points of Shape edited
