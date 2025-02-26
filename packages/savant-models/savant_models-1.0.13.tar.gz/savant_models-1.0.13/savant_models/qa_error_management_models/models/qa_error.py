from typing import List

from pydantic import BaseModel, Field

from savant_models.qa_error_management_models.models.qa_check_result_failed import QACheckResultFailed
from savant_models.utils.base import PyObjectId


class QAError(BaseModel):
    id: PyObjectId = Field(alias="_id")
    sequence_root_id: PyObjectId
    profile_id: PyObjectId
    qa_check_errors: List[QACheckResultFailed]

