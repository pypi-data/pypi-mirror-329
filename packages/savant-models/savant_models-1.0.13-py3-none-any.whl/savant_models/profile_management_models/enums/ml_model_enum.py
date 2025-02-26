from enum import StrEnum


class MLModelEnum(StrEnum):
    MED_SAM = "med"
    SAM2 = "v2"
    MED_SAM2 = "med2"
    SURG_SAM2 = "surg2"
    UNIMATCH = "unimatch"
    CO_TRACKER = "co-tracker"
    CO_TRACKER_KUBRIC = "kubric"
