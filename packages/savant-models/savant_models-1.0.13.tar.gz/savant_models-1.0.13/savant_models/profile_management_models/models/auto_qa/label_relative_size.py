from pydantic import BaseModel

from savant_models.profile_management_models.enums.auto_qa.relative_size import RelativeSize


class LabelRelativeSize(BaseModel):
    label_code: str
    relative_size: RelativeSize
