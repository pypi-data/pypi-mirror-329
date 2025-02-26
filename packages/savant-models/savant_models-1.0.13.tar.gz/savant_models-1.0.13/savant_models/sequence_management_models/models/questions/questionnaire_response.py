from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, Field

from savant_models.sequence_management_models.models.questions.option_response import OptionResponse
from savant_models.utils.base import PyObjectId, BaseModel
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class QuestionnaireResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    question: str

    free_text: Optional[str] = None
    options_selected: Optional[List[OptionResponse]] = None

    date_annotated: datetime
    annotated_by: PyObjectId

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

