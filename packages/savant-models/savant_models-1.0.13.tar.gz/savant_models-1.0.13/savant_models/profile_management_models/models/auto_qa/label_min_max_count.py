from typing import Optional

from pydantic import model_validator, BaseModel


class LabelMinMaxCount(BaseModel):
    label_code: str
    min_count: Optional[int] = None
    max_count: Optional[int] = None

    @model_validator(mode="after")
    def validate_combinations(self):
        min_count = self.min_count
        max_count = self.max_count
        if not min_count and not max_count:
            raise ValueError(f"One of min_count or max_count must be provided")

        return self
