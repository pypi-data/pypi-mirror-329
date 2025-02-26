from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, model_validator

from savant_models.batch_management_models.enums.stereo_orientation_enum import StereoOrientationEnum
from savant_models.batch_management_models.enums.type_of_annotation_enum import TypeOfAnnotationEnum
from savant_models.batch_management_models.models.sub_models.canvas_controls import CanvasControls
from savant_models.utils.response_bodies.response_message import ResponseMessage


class Configuration(BaseModel):
    canvas_controls: Optional[CanvasControls] = CanvasControls()
    orientation: Optional[StereoOrientationEnum] = StereoOrientationEnum.HORIZONTAL
    type_of_annotation: Optional[TypeOfAnnotationEnum] = TypeOfAnnotationEnum.PHASE
    start_time_only: Optional[bool] = False
    default_phase_length: Optional[int] = None

    @model_validator(mode='before')
    def validate_default_phase_length(cls, values):
        start_time_only = values.get("start_time_only")
        default_phase_length = values.get("default_phase_length")

        if default_phase_length and not start_time_only:
            raise HTTPException(
                status_code=400,
                detail=ResponseMessage(
                    success=False,
                    message="default_phase_length must be set when start time only is true",
                ).model_dump(),
            )
        else:
            return values
