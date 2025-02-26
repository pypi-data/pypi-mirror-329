from typing import List, Optional

from pydantic import ConfigDict, Field

from savant_models.utils.base import BaseModel


class Link(BaseModel):
    sub_type: str
    start_from: Optional[List[str]] = Field(alias="from", default=[])
    end_to: Optional[List[str]] = Field(alias="to", default=[])

    model_config = ConfigDict(populate_by_name=True)
