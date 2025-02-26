from pydantic import BaseModel


class BatchesByType(BaseModel):
    variability: int
    survey: int
    video: int
    sequence: int
