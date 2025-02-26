from enum import StrEnum


class ShapeType(StrEnum):
    RECTANGLE = "rectangle"
    KEYPOINT = "keypoint"
    CLOSE_POLYGON = "close_polygon"
    OPEN_POLYGON = "open_polygon"
    POINT = "point"

