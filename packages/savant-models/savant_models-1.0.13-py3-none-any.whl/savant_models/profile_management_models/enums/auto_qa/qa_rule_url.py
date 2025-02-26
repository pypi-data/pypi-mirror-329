from enum import StrEnum


class QARuleURL(StrEnum):
    KEYPOINT_IN_BOUNDING_BOX = "keypoint-in-bounding-box"
    SHAPE_TYPE_COUNT = "shape-type-count"
    SKELETON_SUB_TYPE_COUNT = "skeleton-sub-type-count"
    LABEL_COUNT = "label-count"
    SHAPE_COVERAGE = "shape-coverage"
    LABEL_IN_REGION = "label-in-region"
    LABEL_RELATIVE_SIZE = "label-relative-size"
    LABEL_RELATIVE_POSITION = "label-relative-position"
    LABEL_SUBSET = "label-subset"
    LABEL_MULTIPLE_SUBSETS = "label-multiple-subsets"
    PHASE_LENGTH = "phase-length"
    PHASE_LABEL_COUNT = "phase-label-count"
    PHASE_SECTION_LABEL_COUNT = "phase-section-label-count"
    PHASE_ORDER = "phase-order"
