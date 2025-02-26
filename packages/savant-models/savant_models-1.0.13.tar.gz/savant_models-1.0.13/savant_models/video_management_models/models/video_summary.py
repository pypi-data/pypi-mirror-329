from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.utils.base import PyObjectId
from savant_models.video_management_models.enums.hls_conversion_status import HLSConversionStatus
from savant_models.video_management_models.enums.video_source import VideoSource


class VideoSummary(BaseModel):
    id: str = Field(alias="_id")
    name: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[int] = None
    surgeon_code: Optional[str] = None
    institution_code: Optional[str] = None
    device_uuid: Optional[str] = None
    path_to_mp4: Optional[str] = None
    path_to_hls: Optional[str] = None
    video_tags: Optional[List[dict]] = None
    medical_code: Optional[str] = None
    linked_video_id: Optional[str] = None
    stereo_calibration_path: Optional[str] = None
    datetime_ingested: Optional[datetime] = None
    source: Optional[VideoSource] = None
    created_by: Optional[PyObjectId] = None
    hls_conversion_status: Optional[HLSConversionStatus] = None
    origin_file_project_id: Optional[PyObjectId] = None

    model_config = ConfigDict(populate_by_name=True)
