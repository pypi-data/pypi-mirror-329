from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class WorkflowTrigger(BaseModel):
    workflow: List[str]
    parameters: dict
