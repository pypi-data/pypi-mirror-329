from typing import List

from pydantic import BaseModel, Field

from savant_models.utils.base import PyObjectId
from savant_models.video_management_models.models.deframer_task import DeframerTask
from savant_models.video_management_models.enums.deframer_file_output_type_enum import (
    DeframerFileOutPutTypeEnum,
)
from savant_models.video_management_models.enums.deframer_status_enum import DeframerStatusEnum


class DeframerJob(BaseModel):

    job_id: PyObjectId = Field(default_factory=PyObjectId)
    s3_path: str
    input_bucket: str
    output_bucket_name: str
    file_output: DeframerFileOutPutTypeEnum
    video_id: str
    tasks: List[DeframerTask]
    status: DeframerStatusEnum