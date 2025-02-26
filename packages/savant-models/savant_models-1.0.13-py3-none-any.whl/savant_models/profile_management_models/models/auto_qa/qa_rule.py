from typing import Optional

from pydantic import ConfigDict, Field

from savant_models.profile_management_models.enums.auto_qa.check_level import CheckLevel
from savant_models.profile_management_models.enums.auto_qa.error_level import ErrorLevel
from savant_models.profile_management_models.enums.auto_qa.qa_rule_name import QARuleName
from savant_models.profile_management_models.models.auto_qa.qa_rule_config import QARuleConfig
from savant_models.utils.base import BaseModel, PyObjectId


class QARule(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: QARuleName
    parameters: QARuleConfig.parameters_types
    error_level: Optional[ErrorLevel] = ErrorLevel.ERROR
    check_level: Optional[CheckLevel] = CheckLevel.FRAME

    model_config = ConfigDict(populate_by_name=True)

