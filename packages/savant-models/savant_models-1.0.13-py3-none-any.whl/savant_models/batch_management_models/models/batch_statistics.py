from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.batch_management_models.enums.batch_type import BatchType
from savant_models.organisation_management_models.models.organisation import Organisation
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus
from savant_models.teams_management_models.models.team_summary import TeamSummary
from savant_models.utils.base import PyObjectId


class BatchStatistics(BaseModel):
    id: PyObjectId = Field(alias="_id")

    name: str
    description: Optional[str] = None
    batch_type: Optional[BatchType] = BatchType.SEQUENCE

    project_id: PyObjectId

    creator_uuid: PyObjectId
    date_created: datetime

    profile_id: Optional[PyObjectId] = None

    # Org assigning
    teams_assigned: Optional[List[TeamSummary]] = []

    # Annotator assigning
    auto_assign: Optional[bool] = False

    video_ids: Optional[List[str]] = None
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

    date_first_assigned: Optional[datetime] = None

    date_to_annotate_started: Optional[datetime] = None
    date_to_annotate_ended: Optional[datetime] = None

    date_to_qa_started: Optional[datetime] = None
    date_to_qa_ended: Optional[datetime] = None
    no_sequences_qa: int
    percentage_of_sequences_to_qa: float

    date_to_fix_sent: Optional[datetime] = None
    date_to_fix_started: Optional[datetime] = None
    date_to_fix_ended: Optional[datetime] = None
    percentage_of_sequences_to_review: float

    number_returned_rule: int
    percentage_returned_rule: float

    number_returned_edge_case: int
    percentage_returned_edge_case: float

    number_randomly_selected: int
    percentage_randomly_selected: float

    number_model_selected: int
    percentage_model_selected: float

    number_iterative_selected: int
    percentage_iterative_selected: float

    number_to_fix_sequences: int
    percentage_to_fix_sequences: float

    date_batch_complete: Optional[datetime] = None

    organisations_involved_in_annotations: List[Organisation]

    frames_annotated: int
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

