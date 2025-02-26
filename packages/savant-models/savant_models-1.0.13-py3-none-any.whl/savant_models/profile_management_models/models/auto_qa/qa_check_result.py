from typing import Optional

from pydantic import BaseModel


class QACheckResult(BaseModel):
    qa_check: str
    passed: bool
    object_id: Optional[str]
    message: str
