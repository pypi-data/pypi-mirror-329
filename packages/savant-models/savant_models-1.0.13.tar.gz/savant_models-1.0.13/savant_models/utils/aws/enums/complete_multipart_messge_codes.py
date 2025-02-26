from enum import Enum

class CompleteMultipartMessageCodes(Enum):
    COMPLETED = 200
    SMALL_CHUNK_SIZE = "EntityTooSmall"
    MISSING_PART = "InvalidPart"
    SEQUENCE = "InvalidPartOrder"
    NOT_EXISTS = "NoSuchUpload"
