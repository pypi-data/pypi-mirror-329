from enum import StrEnum


class ModelTypes(StrEnum):
    BATCH = "batch"
    LABEL = "label"
    ORGANISATION = "organisation"
    PROFILE = "profile"
    PROJECT = "project"
    FILE_PROJECT = "file_project"
    SEQUENCE = "sequence"
    MULTI_SEQUENCE = "multi_sequence"
    SKELETON = "skeleton"
    TEAM = "team"
    USER = "user"
    VIDEO = "video"
    QA_ERROR = "qa_error"
    TIME_TRACK = "time_track"
