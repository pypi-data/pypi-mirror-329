from enum import StrEnum


class HLSConversionStatus(StrEnum):
    TRIGGERED = "Triggered"
    DOWNLOADING_MP4 = "Downloading MP4 from S3"
    CONVERTING_TO_HLS = "Converting to HLS"
    UPLOADING_HLS = "Uploading HLS to S3"
    COMPLETE = "Complete"
    FAILED = "Failed"
