from enum import StrEnum


class PostSilhouetteErrorMessageEnum(StrEnum):
    INVALID_HEADERS = "headers provided without authorisation"
    INVALID_CREDENTIALS = "authorisation credentials rejected"
    MAPPING_ERROR = "incorrect mapping"
    INVALID_SEQUENCE = "sequence rejected"
    INVALID_BATCH = "batch rejected"
    PATCH_ERROR = "patch error"
    INVALID_MASK_FORMAT = "incorrect text format, please resend files"
    INVALID_BYTES = "incorrect file format, decode must result in bytes"
    IMAGE_SIZE_EXCEEDED = "image uploaded is not a mask of annotations. please only upload masks"
    IMAGE_DIMENSIONS_ERROR = "image dimensions are wrong. they do not match images within this sequence. please upload a different set of images"
    UPLOAD_ERROR = "s3 upload error"
    MASK_PROCESSING_ERROR = "error processing masks, please resend mask files"
