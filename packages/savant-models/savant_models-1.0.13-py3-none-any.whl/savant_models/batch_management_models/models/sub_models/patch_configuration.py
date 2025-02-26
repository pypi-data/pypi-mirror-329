from typing import Optional

from pydantic import BaseModel

from savant_models.batch_management_models.models.sub_models.canvas_controls import CanvasControls


class PatchConfiguration(BaseModel):
    canvas_controls: Optional[CanvasControls] = None
    default_phase_length: Optional[int] = None
