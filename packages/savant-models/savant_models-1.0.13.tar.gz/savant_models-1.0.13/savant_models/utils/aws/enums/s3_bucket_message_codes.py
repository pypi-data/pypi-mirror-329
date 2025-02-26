from enum import Enum

class S3BucketMessageCodes(Enum):
    BUCKET_EXISTS_GLOBALLY = "403"
    BUCKET_NOT_FOUND = "404"
    BUCKET_EXISTS = 200
    INVALID_NAME = "InvalidBucketName"
    SUCESSFULLY_CREATED = 200

