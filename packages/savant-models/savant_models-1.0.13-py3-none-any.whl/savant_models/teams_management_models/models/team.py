from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.teams_management_models.enums.team_type import TeamType
from savant_models.teams_management_models.models.team_project import TeamProject
from savant_models.utils.base import PyObjectId
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class Team(BaseModel):
    id: PyObjectId = Field(alias="_id")

    type: TeamType

    organisation_id: PyObjectId
    name: str

    creator_id: PyObjectId
    date_created: datetime

    team_members: Optional[List[PyObjectId]] = Field(
        default=[], alias="team_member_ids"
    )

    project_managers: Optional[List[PyObjectId]] = Field(
        default=[], alias="manager_ids"
    )
    annotators: Optional[List[PyObjectId]] = Field(default_factory=list, alias="annotator_ids")

    team_members_count: int = 0
    project_manager_count: int = 0
    annotator_count: int = 0

    to_annotate: bool
    to_qa: bool
    to_review: bool
    to_fix: bool

    projects_count: Optional[int] = 0
    projects: Optional[List[TeamProject]] = []

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})


