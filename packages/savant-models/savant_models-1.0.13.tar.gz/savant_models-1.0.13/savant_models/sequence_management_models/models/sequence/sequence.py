from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, Field

from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.sequence_management_models.enums.type_of_change_enum import TypeOfChangeEnum
from savant_models.sequence_management_models.models.assignees.assignee import Assignee
from savant_models.sequence_management_models.models.assignees.assignees import Assignees
from savant_models.sequence_management_models.models.comments.comment import Comment
from savant_models.sequence_management_models.models.frame.frame import Frame
from savant_models.sequence_management_models.models.frame.frame_image_size import FrameImageSize
from savant_models.sequence_management_models.models.questions.question import Question
from savant_models.sequence_management_models.models.questions.questionnaire_response import QuestionnaireResponse
from savant_models.sequence_management_models.models.tags.sequence_tags import SequenceTags
from savant_models.sequence_management_models.models.video.video_annotation import VideoAnnotation
from savant_models.utils.base import PyObjectId, BaseModel


class Sequence(BaseModel):
    id: PyObjectId = Field(alias="_id")

    sequence_no: int

    # Allow to annotate same set multiple times
    group_id: Optional[PyObjectId] = None

    # External References
    batch_id: Optional[PyObjectId] = None
    auto_assign: Optional[bool] = False

    # video metadata
    video_id: str
    video_annotations: List[VideoAnnotation]
    video_annotations_count: int

    image_size: Optional[FrameImageSize] = None
    feature_set: List[Frame]
    feature_set_count: int

    video_feature_set: Optional[List[Frame]] = []
    video_feature_set_count: Optional[int] = 0

    start_ms: Optional[float] = None
    stop_ms: Optional[float] = None

    video_preview_before_s: Optional[int] = None
    video_preview_after_s: Optional[int] = None

    tags: Optional[SequenceTags] = SequenceTags()

    # access metadata
    creator_id: Optional[PyObjectId] = None
    date_created: datetime

    # assignee
    assignee: Optional[Assignee] = None
    assignees: Optional[Assignees] = Assignees()

    comments: Optional[List[Comment]] = []
    comment_count: Optional[int] = 0

    # Questionnaire
    show_video: Optional[bool] = Field(
        default=True,
        title="Field to be used to determine whether video should be showing during questionnaire",
    )
    preamble: Optional[str] = None
    questions: Optional[List[Question]] = []
    questions_count: Optional[int] = 0
    questionnaire_response: Optional[List[QuestionnaireResponse]] = []

    # Logging
    version: Optional[int] = 1
    author: Optional[PyObjectId] = None
    date_annotated: Optional[datetime] = None
    profile_used: Optional[PyObjectId] = None
    type_of_change: Optional[TypeOfChangeEnum] = None

    # immutability
    root_id: PyObjectId
    previous_id: Optional[PyObjectId] = None
    next_id: Optional[PyObjectId] = None
    status: SequenceStatus
    active: bool

    ext_source: Optional[str] = None

    labels: Optional[List[ProfileTag]] = (
        []
    )  # Change every time frame label of frame changes

    notes: List[str] = []
    linked_root_id: Optional[PyObjectId] = None
    linked_batch_id: Optional[PyObjectId] = None
    linked_video_id: Optional[str] = None

    auto_qa_error_present: Optional[bool] = False

    first_edited: Optional[datetime] = None
    

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})
