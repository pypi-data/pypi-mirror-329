from typing import Optional

from savant_models.profile_management_models.enums.auto_qa.error_level import ErrorLevel
from savant_models.profile_management_models.models.auto_qa.qa_check_result import QACheckResult
from savant_models.utils.base import PyObjectId
from savant_models.profile_management_models.enums.auto_qa.check_level import CheckLevel


class QACheckResultFailed(QACheckResult):
    error_level: ErrorLevel
    check_level:CheckLevel
    user_id: Optional[PyObjectId] = None
    active: bool = True