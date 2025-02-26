from typing import List

from pydantic import BaseModel


class LabelSubsets(BaseModel):
    label_subsets: List[List[str]]
