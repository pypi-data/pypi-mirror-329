from typing import Optional

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    error: str
    detail: Optional[str] = None
    connection: bool

