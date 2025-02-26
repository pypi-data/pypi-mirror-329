from typing import List, Optional

from pydantic import ConfigDict, Field

from savant_models.utils.base import BaseModel
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class QuestionResponseOptions(BaseModel):
    is_multi_choice: bool
    is_free_text: bool
    is_dropdown: bool

    is_free_text_optional: Optional[bool] = None

    select_count: Optional[int] = None

    multi_choice_options: Optional[List[str]] = Field(None, alias="options")
    multi_choice_options_count: Optional[int] = Field(None, alias="options_count")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})
