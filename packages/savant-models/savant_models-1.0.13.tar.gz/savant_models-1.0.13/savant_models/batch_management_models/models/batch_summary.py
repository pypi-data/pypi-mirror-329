from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.batch_management_models.enums.batch_type import BatchType
from savant_models.project_management_models.enums.project_type import ProjectType
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.teams_management_models.models.team_summary import TeamSummary
from savant_models.utils.base import PyObjectId


class BatchSummary(BaseModel):
    id: PyObjectId = Field(alias="_id")

    name: str
    description: Optional[str] = None
    batch_type: Optional[BatchType] = BatchType.SEQUENCE

    project_id: PyObjectId
    project_type: Optional[ProjectType] = None

    project_name: Optional[str] = None

    creator_uuid: PyObjectId
    date_created: datetime

    profile_id: Optional[PyObjectId] = None

    # Org assigning
    teams_assigned: Optional[List[TeamSummary]] = Field(
        alias="team_assignments", default=[]
    )

    # Annotator assigning
    auto_assign: Optional[bool] = False

    video_count: Optional[int] = None
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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

