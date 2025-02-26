from typing import Optional

from pydantic import model_validator, BaseModel


class Length(BaseModel):
    min_length: Optional[int] = None
    max_length: Optional[int] = None

    @model_validator(mode="after")
    def validate_combinations(self):
        min_length = self.min_length
        max_length = self.max_length
        if not min_length and not max_length:
            raise ValueError(f"One of min_length or max_length must be provided")

        return self
