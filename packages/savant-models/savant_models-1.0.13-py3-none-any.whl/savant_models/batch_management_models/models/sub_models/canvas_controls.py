from typing import Optional

from fastapi import HTTPException
from pydantic import field_validator, BaseModel

from savant_models.utils.response_bodies.response_message import ResponseMessage


class CanvasControls(BaseModel):
    brightness: Optional[int] = 100
    contrast: Optional[int] = 100
    thickness: Optional[int] = 5
    opacity: Optional[float] = 0.5
    
    @field_validator("brightness", "contrast")
    def check_brightness_and_contrast_range(cls, value: int) -> int:
        if value not in range(0, 201, 10):
            raise HTTPException(
                status_code=400,
                detail=ResponseMessage(
                    success=False, message="only increments of 10 between from 0 - 200 are allowed"
                ).model_dump(),
            )

        return value

    @field_validator("thickness")
    def check_thickness_range(cls, value: int) -> int:
        if value not in range(1, 11):
            raise HTTPException(
                status_code=400,
                detail=ResponseMessage(
                    success=False, message="thickness must range from 1 - 10"
                ).model_dump(),
            )
        
        return value

    @field_validator("opacity")
    def validate_opacity(cls, value: float) -> float:
        def float_range(start=0, stop=1, step=0.1):
            x = start
            while x <= stop:
                yield round(x, 1)
                x = x + step
            
        if value not in list(float_range()):
            raise HTTPException(
                status_code=400,
                detail=ResponseMessage(
                    success=False, message="only increments of 0.1 between 0 - 1 are allowed"
                ).model_dump(),
            )

        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "brightness": 10,
                "contrast": 10,
                "thickness": 2,
                "opacity": 0.1,
            }
        }