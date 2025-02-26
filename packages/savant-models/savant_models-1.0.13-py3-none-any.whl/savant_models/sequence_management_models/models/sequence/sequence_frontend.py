from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field

from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.sequence_management_models.models.tags.sequence_tags import SequenceTags
from savant_models.utils.base import PyObjectId, BaseModel


class SequenceFrontend(BaseModel):
    """Groups of annotations"""
    id: PyObjectId = Field(alias="_id")

    root_id: PyObjectId
    group_id: Optional[PyObjectId] = None

    sequence_no: int

    # video metadata
    video_id: str
    feature_set_count: int = Field(alias="frame_count")
    video_feature_set_count: Optional[int] = Field(alias="video_frame_count", default=0)

    # assignee
    assignee_id_to_annotate: Optional[PyObjectId] = None
    assignee_id_to_qa: Optional[PyObjectId] = None
    assignee_id_to_review: Optional[PyObjectId] = None
    assignee_id_to_fix: Optional[PyObjectId] = None

    video_annotations_count: int
    questions_count: Optional[int] = 0
    preamble: Optional[str] = None
    comments_count: Optional[int] = 0

    tags: Optional[SequenceTags] = SequenceTags()

    # immutability
    status: SequenceStatus

    auto_qa_error_present: Optional[bool] = False

    first_edited: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

