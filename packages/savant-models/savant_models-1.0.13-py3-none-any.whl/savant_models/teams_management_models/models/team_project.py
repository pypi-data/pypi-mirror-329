from pydantic import ConfigDict, BaseModel, field_validator

from savant_models.utils.base import PyObjectId
from savant_models.utils.validators.check_special_chars import check_special_chars
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class TeamProject(BaseModel):
    batch_id: PyObjectId
    project_name: str
    batch_name: str

    to_annotate: bool
    to_qa: bool
    to_review: bool
    to_fix: bool

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

    @field_validator('project_name', 'batch_name')
    def check_special_chars(cls, v: str):
        return check_special_chars(v)

