from pydantic import BaseModel, Field
from typing_extensions import Annotated


class ShapeCoverage(BaseModel):
    label_code: str
    max_coverage: Annotated[int, Field(strict=True, ge=0, le=100)]
