from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.project_management_models.models.projects_summary import ProjectSummary
from savant_models.teams_management_models.models.team import Team
from savant_models.utils.base import PyObjectId


class Organisation(BaseModel):

    id: PyObjectId = Field(alias="_id")

    name: str

    date_created: datetime
    creator_id: Optional[PyObjectId] = None

    projects: Optional[List[ProjectSummary]] = []
    teams: Optional[List[Team]] = []

    date_last_synced: Optional[datetime] = None
    model_config = ConfigDict(populate_by_name=True)

