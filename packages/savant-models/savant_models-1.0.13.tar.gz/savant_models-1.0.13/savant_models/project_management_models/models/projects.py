from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, BaseModel, Field

from savant_models.batch_management_models.models.batch_frontend import BatchFrontend
from savant_models.profile_management_models.models.profiles import Profile
from savant_models.project_management_models.enums.annotation_type import AnnotationType
from savant_models.project_management_models.enums.project_type import ProjectType
from savant_models.utils.base import PyObjectId


class Project(BaseModel):
    """Project model."""

    id: PyObjectId = Field(alias="_id")

    name: str
    project_type: ProjectType
    annotation_type: AnnotationType

    creator_id: Optional[PyObjectId] = None
    owner_id: Optional[PyObjectId] = None
    date_created: Optional[datetime] = None
    profile_id: Optional[PyObjectId] = None
    profile: Optional[Profile] = None
    description: Optional[str] = None

    batch_count: Optional[int] = 0
    batches: Optional[List[BatchFrontend]] = []

    sequence_count: Optional[int] = 0
    frame_count: Optional[int] = 0
    sequences_in_to_annotate: Optional[int] = 0
    sequences_in_to_qa: Optional[int] = 0
    sequences_in_to_review: Optional[int] = 0
    sequences_in_to_fix: Optional[int] = 0
    sequences_in_completed: Optional[int] = 0

    video_ids: Optional[List[str]] = []
    default_overlapping: Optional[bool] = False
    model_config = ConfigDict(populate_by_name=True)

