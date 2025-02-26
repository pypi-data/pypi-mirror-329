
from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.sequence_management_models.models.assignees.assignee import Assignee
from savant_models.sequence_management_models.models.assignees.assignees import Assignees
from savant_models.sequence_management_models.models.frame.frame_summary import FrameSummary
from savant_models.sequence_management_models.models.questions.question import Question
from savant_models.sequence_management_models.models.questions.questionnaire_response import QuestionnaireResponse
from savant_models.sequence_management_models.models.tags.sequence_tags import SequenceTags
from savant_models.sequence_management_models.models.video.video_annotation import VideoAnnotation
from savant_models.utils.base import PyObjectId



class SequenceSummary(BaseModel):
    """
    Summary of sequence to be shown on project management screen
    """
    id: PyObjectId = Field(alias="_id")

    root_id: Optional[PyObjectId] = None

    group_id: Optional[PyObjectId] = None

    sequence_no: Optional[int] = None
    video_id: str
    status: SequenceStatus

    tags: Optional[SequenceTags] = SequenceTags()

    auto_assign: Optional[bool] = False

    # assignee
    assignee: Optional[Assignee] = None
    assignees: Optional[Assignees] = Assignees()

    video_annotations: List[VideoAnnotation]
    video_annotations_count: int

    questions: Optional[List[Question]] = []
    questions_count: Optional[int] = 0
    questionnaire_response: Optional[List[QuestionnaireResponse]] = []

    comments_count: Optional[int] = 0

    feature_set: List[FrameSummary]
    feature_set_count: int

    video_feature_set: Optional[List[FrameSummary]] = []
    video_feature_set_count: Optional[int] = 0

    ext_source: Optional[str] = None

    labels: Optional[List[ProfileTag]] = (
        []
    )  # Change every time frame label of frame changes

    auto_qa_error_present: Optional[bool] = False

    first_edited: Optional[datetime] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

