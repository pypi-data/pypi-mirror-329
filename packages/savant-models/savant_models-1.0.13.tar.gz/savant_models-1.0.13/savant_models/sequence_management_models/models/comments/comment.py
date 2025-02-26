from datetime import datetime as python_datetime
from typing import Optional, Union, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.sequence_management_models.models.comments.comment_resolve import CommentResolve
from savant_models.sequence_management_models.models.frame.frame_image_size import FrameImageSize
from savant_models.utils.base import PyObjectId


class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    name: Optional[str] = None
    user_id: Optional[PyObjectId] = None
    sequence_id: Optional[PyObjectId] = None
    comment: str
    datetime_edited: Optional[python_datetime] = None
    datetime: Optional[python_datetime] = None
    status: Optional[SequenceStatus] = None
    edited: Optional[bool] = False
    resolve: Optional[CommentResolve] = CommentResolve()
    location: Optional[FrameImageSize] = None
    video_timestamp: Optional[Union[float, List[float]]] = None

    model_config = ConfigDict(populate_by_name=True)
