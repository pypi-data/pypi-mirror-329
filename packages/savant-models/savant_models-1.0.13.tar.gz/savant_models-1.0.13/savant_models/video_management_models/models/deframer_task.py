from typing import Optional
from pydantic import BaseModel

from savant_models.video_management_models.enums.deframer_file_output_type_enum import (
    DeframerFileOutPutTypeEnum,
)

class DeframerTask(BaseModel):

    fps: int
    resize_height: Optional[int] = None
    file_output: Optional[DeframerFileOutPutTypeEnum] = None
    timestamp_start: Optional[int] = None
    timestamp_end: Optional[int] = None

    def __eq__(self, other) -> bool:
        if isinstance(other, DeframerTask):
            return (
                self.fps == other.fps
                and self.resize_height == other.resize_height
                and self.file_output == other.file_output
            )
