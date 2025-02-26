from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from pydantic import ConfigDict, Field, model_validator
from semver import VersionInfo

from savant_models.label_management_models.enums.label_category import LabelCategory
from savant_models.profile_management_models.models.auto_qa.qa_rule import QARule
from savant_models.profile_management_models.models.profile_batch import ProfileBatch
from savant_models.profile_management_models.models.profile_object import ProfileObject
from savant_models.profile_management_models.models.profile_project import ProfileProject
from savant_models.profile_management_models.models.profile_tag import ProfileTag
from savant_models.profile_management_models.models.version_history import VersionHistory
from savant_models.utils.base import BaseModel, PyObjectId
from savant_models.utils.response_bodies.response_message import ResponseMessage
from savant_models.profile_management_models.models.ai_settings import AISettings
from savant_models.profile_management_models.enums.ml_model_enum import MLModelEnum
from savant_models.sequence_management_models.enums.ml_action_enum import MLActionEnum


class Profile(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    root_id: Optional[PyObjectId] = None
    name: str
    version: str
    tags: Optional[List[str]] = []
    video_tags: Optional[List[str]] = None

    creator_uuid: PyObjectId
    date_created: datetime
    parent_profile_uuid: Optional[PyObjectId] = None
    description: str
    objects: Optional[List[ProfileObject]] = None
    version_history: Optional[List[VersionHistory]] = Field(
        [], description="Field contains history of the profile."
    )
    default_count: Optional[int] = 0
    defaults: Optional[List[ProfileProject]] = Field(
        default=[],
        description="List containing projects which use profile as a default.",
    )
    project_count: Optional[int] = 0
    projects: Optional[List[ProfileBatch]] = Field(
        default=[],
        description="List containing all projects/batches that are using profile.",
    )
    sequence_tags: Optional[List[ProfileTag]] = []
    frame_tags: Optional[List[ProfileTag]] = []
    hidden_tags: Optional[List[ProfileTag]] = []
    latest_version: Optional[bool] = True

    labels: List[str]
    categories: List[LabelCategory]

    guideline_url: bool
    organisation_id: Optional[PyObjectId] = None

    rules: Optional[List[QARule]] = []

    ai_settings: Optional[List[AISettings]] = [
        AISettings(
            ml_model=MLModelEnum.SAM2,
            action=MLActionEnum.GENERATE,
            enabled=True,
            is_default=True,
        ),
        AISettings(
            ml_model=MLModelEnum.SAM2, action=MLActionEnum.PROPAGATE, enabled=True
        ),
        AISettings(
            ml_model=MLModelEnum.UNIMATCH, action=MLActionEnum.STEREO_MAP, enabled=True
        ),
    ]

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    def version_must_be_semver(cls, values):
        v = values.get("version")
        version = VersionInfo.is_valid(v)
        if not version:
            raise HTTPException(
                status_code=400,
                detail=ResponseMessage(
                    success=False, message=f"Version '{v}' is invalid SemVer."
                ).model_dump(),
            )
        return values
