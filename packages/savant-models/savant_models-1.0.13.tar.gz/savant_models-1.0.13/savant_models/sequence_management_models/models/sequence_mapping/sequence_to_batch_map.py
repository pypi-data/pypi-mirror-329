from pydantic import ConfigDict, Field

from savant_models.utils.base import BaseModel, PyObjectId


class SequenceToBatchMap(BaseModel):
    id: PyObjectId = Field(alias="_id")
    sequence_id: PyObjectId
    batch_id: PyObjectId

    model_config = ConfigDict(populate_by_name=True)

