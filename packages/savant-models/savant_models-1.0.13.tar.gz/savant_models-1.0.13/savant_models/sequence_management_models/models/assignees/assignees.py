from typing import Optional

from pydantic import ConfigDict, BaseModel, model_validator

from savant_models.sequence_management_models.models.assignees.assignee import Assignee
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class Assignees(BaseModel):  # FrameObject
    """Annotations are shapes with coordinates, label and tags."""
    to_annotate: Optional[Assignee] = None
    to_qa: Optional[Assignee] = None
    to_review: Optional[Assignee] = None
    to_fix: Optional[Assignee] = None

    @model_validator(mode="after")
    def ensure_to_qa_now_to_annotate(self):
        to_annotate, to_qa, to_fix = (
            self.to_annotate,
            self.to_qa,
            self.to_fix
        )
        if to_annotate and to_qa:
            if to_annotate.user_id == to_qa.user_id:
                raise ValueError(f"Could not assign user with id = '{to_qa.user_id}' to both annotate and qa.")
        return self

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})
