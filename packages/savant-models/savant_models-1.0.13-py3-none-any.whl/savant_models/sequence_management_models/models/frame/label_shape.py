from typing import List, Optional, Any

from pydantic import BaseModel

from savant_models.sequence_management_models.enums.ml_action_enum import MLActionEnum
from savant_models.sequence_management_models.models.frame.shape_point import ShapePoint
from savant_models.utils.base import PyObjectId
from savant_models.profile_management_models.enums.ml_model_enum import MLModelEnum


class LabelShape(BaseModel):
    id: Optional[PyObjectId] = None
    type: Optional[str] = None
    sub_type: Optional[str] = None
    points: Optional[List[ShapePoint]] = None
    stereo_id: Optional[Any] = None
    ml_model_source: Optional[MLModelEnum] = None
    action_source: Optional[MLActionEnum] = None
    edited: Optional[bool] = None
    epsilon: Optional[float] = None
    source_shape_id: Optional[PyObjectId] = None
