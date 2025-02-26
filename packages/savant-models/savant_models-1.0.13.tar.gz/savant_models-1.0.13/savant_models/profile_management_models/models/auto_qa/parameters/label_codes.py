from typing import List

from pydantic import BaseModel


class LabelCodes(BaseModel):
    label_codes: List[str]
