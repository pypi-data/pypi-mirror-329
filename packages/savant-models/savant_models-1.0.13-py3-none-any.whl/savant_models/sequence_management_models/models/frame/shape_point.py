from pydantic import BaseModel


class ShapePoint(BaseModel):
    x: float
    y: float
