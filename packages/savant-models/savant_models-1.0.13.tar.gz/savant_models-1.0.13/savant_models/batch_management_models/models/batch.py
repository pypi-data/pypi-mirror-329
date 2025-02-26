from datetime import datetime
from typing import List, Optional


from pydantic import ConfigDict, BaseModel, Field


from savant_models.batch_management_models.enums.batch_type import BatchType
from savant_models.project_management_models.models.projects_summary import ProjectSummary
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.profile_management_models.models.profiles import Profile
from savant_models.sequence_management_models.models.sequence.sequence_summary import SequenceSummary
from savant_models.teams_management_models.models.team_summary import TeamSummary
from savant_models.utils.base import PyObjectId
from savant_models.batch_management_models.models.sub_models.configuration import Configuration


class Batch(BaseModel):
    id: PyObjectId = Field(alias="_id")

    name: str
    description: Optional[str] = None
    batch_type: Optional[BatchType] = BatchType.SEQUENCE
    show_video_preview: Optional[bool] = True

    project_id: PyObjectId
    project: ProjectSummary

    creator_uuid: PyObjectId
    date_created: datetime

    profile_id: Optional[PyObjectId] = None
    profile: Optional[Profile] = None

    # Org assigning
    teams_assigned: Optional[List[TeamSummary]] = []

    # Annotator assigning
    auto_assign: Optional[bool] = False

    video_ids: Optional[List[str]] = None
    video_count: Optional[int] = None
    sequences: Optional[List[SequenceSummary]] = []
    sequence_count: Optional[int] = 0
    frame_count: Optional[int] = 0

    status: Optional[SequenceStatus] = SequenceStatus.TO_ANNOTATE.value

    to_annotate: Optional[int] = 0
    to_qa: Optional[int] = 0
    to_fix: Optional[int] = 0
    to_review: Optional[int] = 0
    completed: Optional[int] = 0

    due_date: Optional[datetime] = None
    to_fix_due_date: Optional[datetime] = None

    overlapping: Optional[bool] = False

    configuration: Optional[Configuration] = Configuration()
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

