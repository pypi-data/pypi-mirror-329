from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel, Field

from savant_models.project_management_models.enums.annotation_type import AnnotationType
from savant_models.project_management_models.enums.project_type import ProjectType
from savant_models.utils.base import PyObjectId


class ProjectSummary(BaseModel):
    """Project model."""
    id: PyObjectId = Field(alias="_id")

    name: str
    project_type: ProjectType
    annotation_type: AnnotationType

    creator_id: Optional[PyObjectId] = None
    owner_id: Optional[PyObjectId] = None
    date_created: Optional[datetime] = None
    profile_id: Optional[PyObjectId] = None
    description: Optional[str] = None

    default_overlapping: Optional[bool] = False

    model_config = ConfigDict(populate_by_name=True)

