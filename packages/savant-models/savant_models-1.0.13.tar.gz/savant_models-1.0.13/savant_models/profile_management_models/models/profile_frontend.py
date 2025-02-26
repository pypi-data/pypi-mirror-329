from typing import List, Optional

from fastapi import HTTPException
from pydantic import ConfigDict, Field, model_validator
from semver import VersionInfo

from savant_models.label_management_models.enums.label_category import LabelCategory
from savant_models.utils.base import BaseModel, PyObjectId
from savant_models.utils.response_bodies.response_message import ResponseMessage


class ProfileFrontend(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    version: str
    projects: Optional[List[str]] = Field(
        default=[],
        description="List containing all projects/batches that are using profile.",
    )
    procedures: Optional[List[str]] = []
    labels: Optional[List[str]] = []
    categories: Optional[List[LabelCategory]] = []
    tags: Optional[List[str]] = []


    @model_validator(mode='before')
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

    model_config = ConfigDict(populate_by_name=True)

