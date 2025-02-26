from enum import StrEnum


class PrivilegeEnum(StrEnum):
    
    BATCHES = "batches"
    PROJECTS = "projects"
    ADMIN = "admin"
    FILE_UPLOADS = "file_uploads"
    LABELS = "labels"
    PROFILES = "profiles"
    VIDEOS = "videos"
