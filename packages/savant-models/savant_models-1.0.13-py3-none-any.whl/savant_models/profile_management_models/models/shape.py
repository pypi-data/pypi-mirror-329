from typing import List, Optional

from pydantic import model_validator, ConfigDict

from savant_models.profile_management_models.enums.shapes import ShapeEnum
from savant_models.profile_management_models.models.link import Link
from savant_models.profile_management_models.models.point import Point
from savant_models.utils.base import BaseModel


class Shape(BaseModel):
    type: ShapeEnum
    color: Optional[str] = None
    points: Optional[List[Point]] = None
    links: Optional[List[Link]] = None
    count: Optional[int] = None

    @model_validator(mode='before')
    def check_points_links_for_keypoint(cls, values):
        """
        Validator will check to ensure points and links are defined
        if type is keypoint for shape
        """
        shape_type = values.get("type")
        if shape_type is None:
            raise ValueError("'type' key not present in shape")

        if shape_type == ShapeEnum.KEYPOINT.value:
            points = values.get("points")
            links = values.get("links")
            if points is None or links is None:
                raise ValueError("Keypoint shape needs both 'points' and 'links' defined.")

        count = values.get("count")
        if count is not None and count < 1:
            raise ValueError("Object count cannot be less than 1.")

        return values

    model_config = ConfigDict(populate_by_name=True)
