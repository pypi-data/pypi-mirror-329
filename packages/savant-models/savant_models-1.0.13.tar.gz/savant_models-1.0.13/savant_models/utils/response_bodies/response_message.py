from typing import Optional
from pydantic import BaseModel


class ResponseMessage(BaseModel):
    success: bool
    message: Optional[str] = None
