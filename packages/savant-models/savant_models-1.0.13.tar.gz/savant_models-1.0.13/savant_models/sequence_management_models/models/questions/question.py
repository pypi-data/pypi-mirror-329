from typing import Optional

from pydantic import ConfigDict, Field

from savant_models.sequence_management_models.models.questions.question_response_options import QuestionResponseOptions
from savant_models.utils.base import PyObjectId, BaseModel
from savant_models.sequence_management_models.enums.sequence_status import SequenceStatus


class Question(BaseModel):
    id: PyObjectId = Field(alias="_id")

    number: int
    question: str
    question_response_options: QuestionResponseOptions

    timestamp_start: Optional[float] = None
    timestamp_end: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={SequenceStatus: lambda v: v.value})

