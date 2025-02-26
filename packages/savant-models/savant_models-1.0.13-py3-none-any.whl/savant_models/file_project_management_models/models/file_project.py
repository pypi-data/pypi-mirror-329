from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.utils.base import PyObjectId
from savant_models.file_project_management_models.enums.file_project_type import FileProjectType
from savant_models.teams_management_models.models.team_summary import TeamSummary


class FileProject(BaseModel):
    file_project_id: PyObjectId = Field(alias="_id")

    name: str
    project_type: Optional[FileProjectType] = FileProjectType.OT.value
    creator_id: Optional[PyObjectId] = None
    owner_id: Optional[PyObjectId] = None
    date_created: Optional[datetime] = None
    description: Optional[str] = None
    teams_assigned: Optional[List[TeamSummary]] = []
    s3_bucket: str
    s3_folder: str

    model_config = ConfigDict(populate_by_name=True)

