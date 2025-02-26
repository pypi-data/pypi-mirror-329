from enum import StrEnum


class DeframerStatusEnum(StrEnum):

    SENT = "sent"
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"
