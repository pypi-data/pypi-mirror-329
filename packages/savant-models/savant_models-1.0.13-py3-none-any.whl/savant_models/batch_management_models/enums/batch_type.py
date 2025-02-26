from enum import StrEnum


class BatchType(StrEnum):
    DEMO = "demo"
    ANNOTATION = "annotation"
    VERIFICATION = "verification"
    VARIABILITY = "variability"
    TRIAL = "trial"
    SURVEY = "survey"
    VIDEO = "video"
    SEQUENCE = "sequence"
    SILHOUETTE = "silhouette"
    ACTIVE = "active"
    COOPERATIVE = "cooperative"
    STEREO = "stereo"
