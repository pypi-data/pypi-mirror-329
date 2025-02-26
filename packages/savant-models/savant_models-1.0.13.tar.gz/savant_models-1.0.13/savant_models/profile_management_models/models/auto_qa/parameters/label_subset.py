from typing import List

from pydantic import BaseModel


class LabelSubset(BaseModel):
    label_subset: List[str]
