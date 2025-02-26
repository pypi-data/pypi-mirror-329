from enum import StrEnum


class QARuleName(StrEnum):
    KEYPOINT_IN_BOUNDING_BOX = "Keypoint In Bounding Box"
    SHAPE_TYPE_COUNT = "Shape Type Count"
    SKELETON_SUB_TYPE_COUNT = "Skeleton Sub Type Count"
    LABEL_COUNT = "Label Count"
    SHAPE_COVERAGE = "Shape Coverage"
    LABEL_IN_REGION = "Label In Region"
    LABEL_RELATIVE_SIZE = "Label Relative Size"
    LABEL_RELATIVE_POSITION = "Label Relative Position"
    LABEL_SUBSET = "Label Subset"
    LABEL_MULTIPLE_SUBSETS = "Label Multiple Subsets"
    PHASE_LENGTH = "Phase Length"
    PHASE_LABEL_COUNT = "Phase Label Count"
    PHASE_SECTION_LABEL_COUNT = "Phase Section Label Count"
    PHASE_ORDER = "Phase Order"
