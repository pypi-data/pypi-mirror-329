
from enum import StrEnum


class PostSilhouetteClientMessageEnum(StrEnum):
    CONNECTED = "connection accepted"
    GET_SEQUENCE_ID = "please provide a sequence id"
    SEND_MASKS = "please send mask files"
    VALIDATION_COMPLETE = "files validation complete, upload successful"
